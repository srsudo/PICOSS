"""PICOSS interface main script.

This script allows the user to run the GUI interface. It is assumed that the seismic data streams has been previously 
processed and stored in an correct format within the data folder (e.g: miniseed), or accessed via data repositories,
such as IRIS. In practice, if the data can be stored in NumPy format, it can be read nby PICOSS. 

PLease, make sure the required modules listed in "requirements.txt" are installed within the working Python environment 
you are interfacing PICOSS with. 

Additional functionalities are included to support the main program, including: 

    * 
    *
    *
"""

# Graphical packages
from PyQt4 import QtGui, QtCore
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# Own packages
from picos_gui import picoss_main
from picos_gui import picoss_func

import picoss_config

# Numerical Computation packages
import math
import numpy as np

# System packages
import os
import sys
import time
import multiprocessing

# Seismology
import obspy

# Others
import gc
import webbrowser
gc.enable()


class Picos(QtGui.QMainWindow, picoss_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Picos, self).__init__(parent)
        self.setupUi(self)
        self.create_menus()

        self.current_label = ""
        self.trace_loaded = None
        self.trace_loaded_filename = ""

        # STATION, CHANNEL NETWORK AND LOCATION CODES
        self.station = None
        self.channel = None
        self.network = None
        self.location = None
        self.component = None
        self.trace_number = 0  # by default

        self.day_of_the_year = None

        # String to save
        self.destination_folder = picoss_config.destination_folder

        self.toSave = None

        self.fm = 0  # Sampling Frequency, depends of the active trace
        self.ts = 0  # Time frequency interval. Depends of the trace
        self.fft_points = picoss_config.nfft  # Number of the fft points.
        self.highpass_freq = picoss_config.highpass  # highpass frequency default for the active trace.

        self.stream = None
        self.active_trace = None
        self.x1, self.x2 = 0, 0

        self.first_ticked = 0
        self.last_ticked = 0

        # dates for interfacing with the servers
        self.start_data = None
        self.end_data = None
        self.connective_client = None

        # axis for the graphs
        self.ax = None
        self.ax1 = None
        self.ax2 = None

        # lta_sta
        self.on_of = None

        # buttons action definition
        self.btnfft.clicked.connect(self.pinta_fft)  # button for the FFT
        self.btnspecgram.clicked.connect(self.pinta_spectrogram)  # button for the specgram
        self.buttonGroup.buttonClicked.connect(self.handleButtonClicked)  # button for the labels

        self.submitwindow.clicked.connect(self.submit_current_window)
        self.submittrace.clicked.connect(self.submit_current_trace)

        # ExtraMenus
        self.isolated_menu = None
        self.connection_menu = None

        self.show()  # Show the interface

    def create_menus(self):
        """
        Function to create the selected main menus in our interface. Functionality is appended on-the-fly with other
        function calls, along with expanded capabilities.
        """
        # File menu
        self.file_menu = QtGui.QMenu('&Data', self)
        self.file_menu.addAction('&Select From Folder', self.show_isolated,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_F)

        self.file_menu.addAction('&Request From Server', self.show_connection,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_R)

        self.file_menu.addAction('&Frequency and Filtering', self.show_auxiliar_menu)

        self.file_menu.addAction('&Quit', self.close,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # Functionalities with extra visualizations

        self.menu_howTo = QtGui.QMenu("&Extra info", self)
        self.menu_howTo.addAction('&Visualize other components', self.show_components_menu)
        self.menu_howTo.addAction('&Visualize other stations', self.show_other_stations)
        self.menuBar().addMenu(self.menu_howTo)

        # Functionalities for the Detection
        self.menu_detection = QtGui.QMenu("&Detection", self)
        self.menu_detection.addAction('&STA/LTA', self.show_STALTA)
        self.menu_detection.addAction('&AMPA', self.show_AMPA)
        self.menu_detection.addAction('&Load picking file', self.load_picking_results)
        self.menuBar().addMenu(self.menu_detection)

        # Zoom and span buttons
        self.menu_toggle = QtGui.QMenu("&Zoom&Span", self)
        self.menu_toggle.addAction("Zoom", self.toggle_zoom, QtCore.Qt.CTRL + QtCore.Qt.Key_Z)
        self.menu_toggle.addAction("Span", self.toggle_pan, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.menu_toggle.addAction("Main View", self.toggle_view, QtCore.Qt.CTRL + QtCore.Qt.Key_U)
        self.menuBar().addMenu(self.menu_toggle)

        # We will deprecate this in a future.
        self.menu_about = QtGui.QMenu("&About", self)
        self.menu_about.addAction("How To Use this interface", self.pop_howtoMenu)
        self.menu_about.addAction("Volcano-Seismology", self.pop_seismology)
        self.menu_about.addAction("&About PICOSS", self.pop_about)
        self.menuBar().addMenu(self.menu_about)

        # Main selector for the trace.
        self.selector = None
        self.toolbar_trace = None

    def pop_howtoMenu(self):
        webbrowser.open(os.path.join(picoss_config.webpage_project, "info", "howto"))

    def pop_about(self):
        webbrowser.open(os.path.join(picoss_config.webpage_project, "info", "about.ipynb"))

    def pop_seismology(self):
        webbrowser.open(os.path.join(picoss_config.webpage_project, "info", "seismology"))

    def check_plots(self):
        """Function to axis plots."""
        if self.ax is None:
            pass

    def show_isolated(self):
        """
        Function to load the data from folder whilst updating the parent.
        """
        self.isolated_menu = picoss_func.WindowLoadFolder(self)
        self.isolated_menu.show()

    def show_components_menu(self):
        pass
        #self.component_menu = ChildWindowComponents(self)
        #self.component_menu.show()

    def show_other_stations(self):
        pass
        #self.stations_window = ChildWindowStations(self)
        #self.stations_window.show()

    def show_STALTA(self):
        pass

    def show_AMPA(self):
        pass

    def plot_stalta(self):

        dict_loaded = self.load_pickle(self.trace_loaded_filename)
        datos = obspy.core.trace.Trace(data=dict_loaded['data'])

        self.active_trace = datos.copy()
        self.stream = obspy.core.stream.Stream(traces=[self.active_trace])

        self.on_of = dict_loaded['on_of']

        # self.fm = 100.0 # we need to save the FM in the sta/lta dictionary. MODIFY THIS ON THE PIPELINE
        if "fm" in dict_loaded.keys():
            self.fm = float(dict_loaded['fm'])
        else:
            self.fm = 100.0

        time_Vector = np.linspace(0, self.active_trace.data.shape[0] / self.fm, num=self.active_trace.data.shape[0])

        self.toSave = "%s_%s_%s_%s_%s_%s.save" % (
            self.network, self.station, self.channel, self.location, self.day_of_the_year, time_Vector.shape[0])

        # create an axis
        self.ax = self.figura_traza.add_subplot(111)
        # discards the old graph
        self.ax.cla()
        self.ax.plot(time_Vector, self.active_trace)
        self.ax.toolbar_trace = NavigationToolbar(self.canvas_traza, self)

        self.selector = RectangleSelector(self.ax, self.line_select_callback,
                                          drawtype='box', useblit=True, button=[1],
                                          minspanx=5, minspany=5, spancoords='pixels',
                                          interactive=True)
        ymin, ymax = self.ax.get_ylim()
        self.ax.vlines(self.on_of[:, 0] / self.fm, ymin, ymax, color='r', linewidth=1)
        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()

    def load_picking_results(self):
        self.stalta = ChildWindow(self)
        self.stalta.sta_lta = True
        self.stalta.show()

    def peak_to_peak(self):

        valor = np.asarray([self.x1, self.x2]) * self.fm
        chunkPlot = self.active_trace.data[int(valor[0]):int(valor[1])]
        """
        print np.asarray(chunkPlot)
        print np.amin(chunkPlot)
        print np.amax(chunkPlot)
        """
        return np.abs(np.amax(chunkPlot) - np.amin(chunkPlot))

    def check_overlapping(self, v1, v2):
        if (float(self.first_ticked) <= v1 <= float(self.last_ticked)):
            return True
        elif (float(self.first_ticked) <= round(self.x2, 2) <= float(self.last_ticked)):
            return True
        else:
            return False

    def submit_current_window(self):
        # check which radio button is selected
        if self.current_label == "":
            self.msg_box("Can not submit if no label is selected", "Please, select one or change window.")
        else:
            label = self.current_label
            alumni = self.comments.text()
            slider = self.qualityslider.value()
            start, end = str(round(self.x1, 2)), str(round(self.x2, 2))
            peakAmpl = str(round(self.peak_to_peak(), 2))
            duration = str(abs(float(end) - float(start)))

            if self.check_overlapping(round(self.x1, 2), round(self.x2, 2)):
                self.msg_box("Current window overlap previous one", "Please, move the sliding window.")

            else:
                currentRowCount = self.table_trace.rowCount()
                self.table_trace.insertRow(currentRowCount)
                self.table_trace.setItem(currentRowCount, 0, QtGui.QTableWidgetItem(start))
                self.table_trace.setItem(currentRowCount, 1, QtGui.QTableWidgetItem(end))
                self.table_trace.setItem(currentRowCount, 2, QtGui.QTableWidgetItem(label))
                self.table_trace.setItem(currentRowCount, 3, QtGui.QTableWidgetItem(peakAmpl))
                self.table_trace.setItem(currentRowCount, 4, QtGui.QTableWidgetItem(duration))
                self.table_trace.setItem(currentRowCount, 5, QtGui.QTableWidgetItem(str(slider)))
                self.table_trace.setItem(currentRowCount, 6, QtGui.QTableWidgetItem(alumni))

                # now we add the last xticks window
                self.first_ticked = start
                self.last_ticked = end

                # self.
                new_job = multiprocessing.Process(target=self.clean_figures(), args=())
                new_job.start()

                redraw = multiprocessing.Process(target=self.redraw_trace(), args=())
                redraw.start()
                time.sleep(2)

        gc.collect()

    def handleButtonClicked(self, button):
        # print('"%s" was clicked' % button.text())
        value = button.text().split(" ")[-1]
        self.current_label = value[1:-1]

    def submit_current_trace(self):
        allRows = self.table_trace.rowCount()
        if self.ax is None or allRows == 0:
            self.msg_box("No current trace is plotted", "Data can not be submitted")
        else:
            data = []
            data.append((self.start_data, self.end_data))
            for row in xrange(0, allRows):
                start_toSave = str(self.table_trace.item(row, 0).text())
                end_toSave = str(self.table_trace.item(row, 1).text())
                label_toSave = str(self.table_trace.item(row, 2).text())
                peak_toSave = str(self.table_trace.item(row, 3).text())
                duration_toSave = str(self.table_trace.item(row, 4).text())
                slides_toSave = str(self.table_trace.item(row, 5).text())
                alumni_toSave = str(self.table_trace.item(row, 6).text())  # qtsting
                new = [start_toSave, end_toSave, label_toSave, peak_toSave, duration_toSave, slides_toSave,
                       alumni_toSave]
                data.append(new)

            self.save_pickle(self.toSave, data)
            self.clean_table()
            self.clean_figures()
            self.clean_points()
            self.figura_traza.clf()
            self.canvas_traza.draw()
            gc.collect()

    def clean_table(self):
        self.table_trace.clearContents()
        self.table_trace.setRowCount(0)

    def clean_points(self):
        self.x1 = 0
        self.x2 = 0
        self.first_ticked = 0
        self.last_ticked = 0

    def clean_figures(self):
        self.figura_spectrograma.clf()
        self.figura_fft.clf()
        self.canvas_specgram.draw()
        self.canvas_fft.draw()

    def redraw_trace(self):
        # print self.ax.lines
        [self.ax.lines[-1].remove() for x in range(2)]
        # self.ax.lines[-1].remove()
        # self.ax.lines[-1].remove()
        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()

    def reset_interactive(self):
        mode = self.ax.get_navigate_mode()
        if mode == "ZOOM":
            self.toggle_zoom()
        elif mode == "PAN":
            self.toggle_pan()
        else:
            pass

    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        # put the previous one to zero, just in case
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, self.y2 = erelease.xdata, erelease.ydata

    def toggle_zoom(self):
        if self.ax is not None:
            self.ax.toolbar_trace.zoom()

    def toggle_pan(self):
        if self.ax is not None:
            self.ax.toolbar_trace.pan()

    def toggle_view(self):
        if self.ax is not None:
            self.ax.toolbar_trace.home()

    def show_connection(self):
        self.connection_menu = ChildWindowConnection(self)
        self.connection_menu.show()

    def show_auxiliar_menu(self):
        self.connection_menu = ChildWindowAuxiliary(self)
        self.connection_menu.show()

    def merge_numpy(self, stream):
        data = []
        for k in xrange(len(stream)):
            data.append(stream[k].data)

        return np.asarray(np.hstack(data))

    def plot_from_file(self):
        self.stream = obspy.read(self.trace_loaded_filename)
        if self.ax is not None:
            self.clean_figures()
            self.reset_interactive()

        self.prepare_stream()

    def prepare_stream(self, bandpass=None):
        # st = obspy.read(self.trace_loaded)
        # st = self.read_file(self.trace_loaded_filename)
        # print type(self.trace_loaded)
        # self.trace_loaded_filename = str(self.trace_loaded)

        st = self.stream.copy()  # we need to make a copy to preserve original data in case we need to filter.

        # self.trace_loaded = st
        # filtered = st.filter("highpass", freq=0.5)
        if bandpass == None:
            filtered = st.filter("highpass", freq=self.highpass_freq)
        else:
            filtered = st.filter("bandpass", freqmin=bandpass[0], freqmax=bandpass[1])

        # self.trace_loaded = filtered.merge(method=0,fill_value='interpolate', interpolation_samples=-1)
        self.trace_loaded = filtered.merge(method=0)
        self.trace_loaded = self.trace_loaded._cleanup()
        self.active_trace = self.trace_loaded[0]

        if isinstance(self.trace_loaded, obspy.core.stream.Stream):

            self.fm = self.active_trace.stats.sampling_rate

            self.start_data = self.active_trace.stats.starttime
            self.end_data = self.active_trace.stats.endtime
            self.day_of_year = self.start_data.strftime('%j')
            duration = int(math.ceil(self.end_data - self.start_data))  # duration in seconds, rounded up

            if self.fm == 75.19:
                self.fm = 75.0

            self.ts = 1 / float(self.fm)
            # We save it same format as Silvio servers: NETWORK, STATION CHANNEL, LOCATION, YEAR, DAY_OF_THE_YEAR

            self.toSave = "%s_%s_%s_%s_%s_%s_%s.save" % (self.network, self.station, self.channel, self.location,
                                                         self.start_data.year, self.day_of_the_year, duration)

            # new_job = multiprocessing.Process(target=self.pinta_trace(), args= ())
            # new_job.start()
            # time.sleep(2)

            self.pinta_trace()

        else:
            raise NotImplementedError

    def plot_from_server(self):
        filtered = self.trace_loaded.filter("highpass", freq=0.5)

        self.trace_loaded = filtered.merge(method=1)
        self.active_trace = self.trace_loaded[0]

        self.fm = self.active_trace.stats.sampling_rate
        self.ts = 1 / float(self.fm)

        self.start_data = self.active_trace.stats.starttime
        self.end_data = self.active_trace.stats.endtime
        self.day_of_year = self.start_data.strftime('%j')
        duration = int(math.ceil(self.end_data - self.start_data))  # duration in seconds, rounded up

        self.toSave = "%s_%s_%s_%s_%s_%s_%s.save" % (self.network, self.station, self.channel, self.location,
                                                     self.start_data.year, self.day_of_the_year, duration)

        new_job = multiprocessing.Process(target=self.pinta_trace(), args=())
        new_job.start()
        time.sleep(2)
        # self.pinta_trace()

    def pinta_trace(self):
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        if self.ax is not None:
            self.ax.cla()

        trace = self.active_trace.data
        time_Vector = np.linspace(0, len(trace) / self.fm, num=len(trace))
        # create an axis
        self.ax = self.figura_traza.add_subplot(111)
        # discards the old graph
        self.ax.cla()
        self.ax.plot(time_Vector, trace)
        self.ax.toolbar_trace = NavigationToolbar(self.canvas_traza, self)

        self.selector = RectangleSelector(self.ax, self.line_select_callback,
                                          drawtype='box', useblit=True, button=[1],
                                          minspanx=5, minspany=5, spancoords='pixels',
                                          interactive=True)

        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()
        gc.collect()

    def pinta_spectrogram(self):
        # print self.x1, self.x2
        if (self.x1 <= 0) or (self.x2 >= len(self.active_trace.data)) or (self.y1 == self.y2):
            self.msg_box("No active window is selected",
                         "Please, select one point the trace and drag along the time axis.")
        else:
            if self.ax1 is not None:
                self.ax1.cla()
                self.figura_spectrograma.clf()

            signal = self.active_trace.data
            valor = np.asarray([self.x1, self.x2]) * self.fm
            chunkPlot = signal[int(valor[0]):int(valor[1])]
            self.ax1 = self.figura_spectrograma.add_subplot(111)
            self.ax1.cla()
            self.ax1.specgram(chunkPlot.flatten(), NFFT=64, Fs=self.fm, noverlap=32, cmap='jet')
            self.ax1.set_ylim(0, 20)
            self.canvas_specgram.draw()

    def pinta_fft(self):
        # print self.x1, self.x2
        if (self.x1 <= 0) or (self.x2 >= len(self.active_trace.data)) or (self.y1 == self.y2):
            self.msg_box("No active window is selected",
                         "Please, select one point the trace and drag along the time axis.")
        else:
            if self.ax2 is not None:
                self.ax2.cla()

            ##### FFT computations
            signal = self.active_trace.data
            valor = np.asarray([self.x1, self.x2]) * self.fm
            chunkPlot = signal[int(valor[0]):int(valor[1])]

            # SOme problems with masked arrays on some volcanoes.
            if np.ma.isMaskedArray(chunkPlot):
                # chunkPlot = np.ma.getdata(chunkPlot)
                print "converting"
                print np.isnan(chunkPlot).any()
                xi = np.arange(len(chunkPlot))
                mask = np.isfinite(chunkPlot)
                chunkPlot = np.interp(xi, xi[mask], chunkPlot[mask])
                print np.isnan(chunkPlot).any()

            n = len(chunkPlot)  # length of the signal
            k = np.arange(n)

            T = n / self.fm
            frq = k / T  # two sides frequency range
            frq = frq[range(n / 2)]  # one side frequency range
            Y = np.fft.fft(chunkPlot) / n  # fft computing and normalization
            Y = Y[range(n / 2)]

            # ax2 = self.figura_fft.add_subplot(111)
            self.ax2 = self.figura_fft.add_subplot(111)
            self.ax2.cla()
            self.ax2.set_xlabel('Freq (Hz)')

            if self.loglogaxis.isChecked():
                self.ax2.set_ylabel('log(|Y(freq)|)')
                self.ax2.semilogy(frq[1:], np.abs(Y)[1:], 'r')
                self.canvas_fft.draw()

            else:
                self.ax2.set_ylabel('|Y(freq)|')
                self.ax2.plot(frq[1:], abs(Y)[1:], 'r')
                self.ax2.set_xlim(0, 20)
                self.canvas_fft.draw()

    def load_pickle(self, filename):

        try:
            f = open(filename, 'rb')
            loaded_object = cPickle.load(f)
            f.close()
            return loaded_object
        except (IOError, OSError) as e:
            pass



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = Picos()
    ret = app.exec_()
    sys.exit(ret)
