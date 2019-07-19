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
from menus import DialogFiltering
from menus import DialogComponents
from menus import DialogConnection
from menus import DialogFolder
from menus import DialogStations


# Numerical Computation packages
import math
import numpy as np
import utils

# System packages
import os
import sys
import time
import multiprocessing

# Seismology
import obspy
from obspy import UTCDateTime

# Others
import webbrowser
import gc
gc.enable()

webpage_project = "https://github.com/srsudo/picos/tree/master"


class MainWindow(QtGui.QMainWindow, picoss_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
        self.destination_folder = "segmented_data"

        if os.path.isdir(self.destination_folder):
            pass
        else:
            os.mkdir(self.destination_folder)

        self.toSave = None

        self.fm = 0  # Sampling Frequency, depends of the active trace
        self.ts = 0  # Time frequency interval. Depends of the trace
        self.fft_points = 600  # Number of the fft points.
        self.highpass_freq = 0.5  # highpass frequency for the active trace.

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

        self.show()

        # ExtraMenus
        self.isolated_menu = None
        self.connection_menu = None

    def save_pickle(self, file, data):
        f = open(os.path.join(self.destination_folder, file), 'wb')
        cPickle.dump(data, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()

    def msg_box(self, mensaje1, mensaje2):

        msgBox = QtGui.QMessageBox(self)
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText(mensaje1)
        msgBox.setInformativeText(mensaje2)
        msgBox.addButton(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        if ret == QtGui.QMessageBox.Ok:
            return True

    def pop_howtoMenu(self):
        webbrowser.open(os.path.join(webpage_project, "info", "howto"))

    def pop_about(self):
        webbrowser.open(os.path.join(webpage_project, "info", "about.ipynb"))

    def pop_seismology(self):
        print os.path.join(webpage_project, "info", "seismology")

    def create_menus(self):
        self.file_menu = QtGui.QMenu('&Data', self)
        self.file_menu.addAction('&Select From Folder', self.show_isolated,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_F)

        self.file_menu.addAction('&Request From Server', self.show_connection,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_R)

        self.file_menu.addAction('&Frequency and Filtering', self.show_auxiliar_menu)

        self.file_menu.addAction('&Quit', self.close,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)

        self.menuBar().addMenu(self.file_menu)

        self.menu_howTo = QtGui.QMenu("&Extra info", self)
        self.menu_howTo.addAction('&Visualize other components', self.show_components_menu)
        self.menu_howTo.addAction('&Visualize other stations', self.show_other_stations)
        self.menuBar().addMenu(self.menu_howTo)

        self.menu_detection = QtGui.QMenu("&Detection")
        self.menu_detection.addAction('&STA/LTA', self.show_STALTA)
        self.menu_detection.addAction('&Load picking file', self.load_picking_results)
        self.menuBar().addMenu(self.menu_detection)

        self.menu_toggle = QtGui.QMenu("&Zoom&Span", self)
        self.menu_toggle.addAction("Zoom", self.toggle_zoom, QtCore.Qt.CTRL + QtCore.Qt.Key_Z)
        self.menu_toggle.addAction("Span", self.toggle_pan, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.menu_toggle.addAction("Main View", self.toggle_view, QtCore.Qt.CTRL + QtCore.Qt.Key_U)

        self.menuBar().addMenu(self.menu_toggle)
        self.menu_about = QtGui.QMenu("&About", self)
        self.menu_about.addAction("How To Use this interface", self.pop_howtoMenu)
        self.menu_about.addAction("Volcano-Seismology", self.pop_seismology)
        self.menu_about.addAction("&About PICOSS", self.pop_about)
        self.menuBar().addMenu(self.menu_about)

        # the selector
        self.selector = None
        self.toolbar_trace = None

    def check_plots(self):
        if self.ax is None:
            pass

    def show_components_menu(self):
        self.component_menu = ChildWindowComponents(self)
        self.component_menu.show()

    def show_other_stations(self):
        self.stations_window = ChildWindowStations(self)
        self.stations_window.show()

    def show_STALTA(self):
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

    def show_isolated(self):
        self.isolated = ChildWindow(self)
        self.isolated.show()

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


class ChildWindow(QtGui.QMainWindow, DialogFolder.Ui_MainWindow):
    def __init__(self, parent):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        # Here, we should add the listener
        self.pushButton_4.clicked.connect(self.get_info)
        self.pushButton_3.clicked.connect(self.load_isolated)
        self.filename = None
        self.job = None
        self.sta_lta = False

    def get_info(self):
        if self.filename is None:
            self.parent().msg_box("Can not submit without a file!", "Choose one file")
        elif self.filename is not None and self.sta_lta:
            self.update_parent_fromText()
            self.parent().plot_stalta()
            self.close()

        else:
            # In case the file is chosen, we get the attributes we want (i should change this)
            self.update_parent_fromText()
            self.parent().plot_from_file()
            self.close()

    def update_parent_fromText(self):
        self.parent().station = str(self.station_2.text())
        self.parent().channel = str(self.channel_2.text())
        self.parent().network = str(self.network_2.text())
        self.parent().location = str(self.location_2.text())
        self.parent().day_of_the_year = str(self.day_of_the_year.text())
        self.parent().trace_loaded_filename = str(self.filename)

    def autocomplete(self, string):
        arr = string.split("/")[-1].split(".")
        if len(arr) != 0:
            self.network_2.setText(arr[0])
            self.station_2.setText(arr[1])
            self.channel_2.setText(arr[3])
            self.day_of_the_year.setText(arr[-1])

    def load_isolated(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/'))
        self.label_filename_2.setText(self.filename)
        self.autocomplete(self.filename)


class ChildWindowConnection(QtGui.QMainWindow, DialogConnection.Ui_MainWindow):
    def __init__(self, parent):
        super(ChildWindowConnection, self).__init__(parent)
        self.setupUi(self)
        self.requestbutton.clicked.connect(self.requestdata)
        self.cnt = None

    def select_client(self, client):
        if client == 'Earthworm':
            from obspy.clients.earthworm import Client as EClient
            self.cnt = EClient(self.ip_address, int(self.port))
        elif client == 'Seedlink':
            from obspy.clients.seedlink import Client as SClient
            self.cnt = SClient(self.ip_address, int(self.port))
        elif client == 'FDSN':
            pass
            # elf.cnt = FClient(self.ip_address, self.port)
        elif client == 'arclink':
            pass
            # self.cnt = AClient(self.ip_address, int(self.port))
        else:
            from obspy.clients.iris import Client as IClient
            self.cnt = IClient("IRIS")

    def requestdata(self):
        self.ip_address = self.ip_c.text()
        self.port = int(self.port_c.text())

        """
        if (ip_address == '' or port == ''):
            self.parent().msg_box("IP address or port seems empty", "Please, enter data correctly!")
        else:
        """

        self.parent().network = str(self.network_c.text())
        self.parent().station = str(self.station_c.text())
        self.parent().channel = str(self.channel_c.text())
        self.parent().location = str(self.location_c.text())
        # self.parent().component = str(self.component_c.text())
        # self.parent().trace_number = str(self.numtraceBox.value())

        self.parent().start_data = UTCDateTime((self.startTime.dateTime().toPyDateTime()))
        self.parent().end_data = UTCDateTime((self.endTime.dateTime().toPyDateTime()))

        # request the data
        self.select_client(str(self.comboServers.currentText()))
        st = self.cnt.get_waveforms(self.parent().network, self.parent().station,
                                    self.parent().location,
                                    self.parent().channel,
                                    self.parent().start_data,
                                    self.parent().end_data)

        # st = "9702-10-1441-50S.MVO_18_1" #this is only from test!!
        self.parent().trace_loaded = st
        self.parent().stream = st
        self.close()
        gc.collect()
        self.parent().plot_from_server()


class ChildWindowAuxiliary(QtGui.QMainWindow, DialogFiltering.Ui_MainWindow):
    def __init__(self, parent):
        super(ChildWindowAuxiliary, self).__init__(parent)
        self.setupUi(self)
        self.new_fm.setText(str(self.parent().fm))
        self.highpass_new.setText(str(self.parent().highpass_freq))
        # self.loadfile.clicked.connect(self.load_isolated)
        self.replot.clicked.connect(self.plot)
        self.filename_current_trace.setText(self.parent().trace_loaded_filename)

        self.button_bandpass.clicked.connect(self.enablebandpass)
        self.button_highpass.clicked.connect(self.enablehighpass)

    def check_digits(self, number):
        if number.replace('.', '', 1).isdigit():
            return True
        elif number.isdigit():
            return True
        else:
            return False

    def check_emptiness(self, param):
        if param not in ['\n', '\r\n']:
            return True
        else:
            return False

    def check_param(self, param):
        if self.check_digits(param) and self.check_emptiness(param):
            return True
        else:
            return False

    def enablebandpass(self):
        self.bp_highfreq.setEnabled(True)
        self.bp_downfreq.setEnabled(True)
        self.highpass_new.setEnabled(False)

    def enablehighpass(self):
        self.highpass_new.setEnabled(True)
        self.bp_highfreq.setEnabled(False)
        self.bp_downfreq.setEnabled(False)

    def plot(self):

        self.parent().reset_interactive()
        fm = str(self.new_fm.text())
        freq_but = str(self.highpass_new.text())

        if self.button_bandpass.isChecked() and self.check_param(fm):
            freq_high = str(self.bp_highfreq.text())
            freq_low = str(self.bp_downfreq.text())
            if (self.check_param(freq_high) and self.check_param(freq_low)) \
                    and (float(freq_high) > float(freq_low)):
                # clean stuff and make it run
                self.parent().clean_figures()
                self.parent().prepare_stream(bandpass=[float(freq_low), float(freq_high)])
                self.close()

        elif self.button_highpass.isChecked() and self.check_param(fm):
            if self.check_param(fm) and self.check_param(freq_but):
                self.parent().fm = float(fm)
                self.parent().clean_figures()
                self.parent().highpass_freq = float(freq_but)
                self.parent().prepare_stream()
                self.close()
            else:
                pass


class ChildWindowComponents(QtGui.QMainWindow, DialogComponents.Ui_MainWindow):
    def __init__(self, parent):
        super(ChildWindowComponents, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        self.pushButton_3.clicked.connect(self.load_data)
        self.pushfirst.clicked.connect(self.plot_comp)
        self.current_x1, self.current_x2 = self.parent().x1, self.parent().x2
        self.current_fm = self.parent().fm
        self.label_t0.setText(str(self.current_x1))
        self.label_t1.setText(str(self.current_x2))

        self.active_component = None
        self.trace_component = None
        self.filename_c = None

    def load_data(self):
        self.refresh()
        self.filename_c = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/'))
        self.label_loaded.setText(self.filename_c)
        self.active_component = obspy.read(self.filename_c)
        self.process_component()

        # component_job = multiprocessing.Process(target=self.process_component)
        # component_job.start()

    def process_component(self):
        filtered = self.active_component.filter("highpass", freq=self.parent().highpass_freq)
        self.active_component = filtered.merge(method=0, fill_value='interpolate')
        self.trace_component = self.active_component[0]
        return self.trace_component

    def select_from_component(self, t0, t1, fm):
        trace_c = self.trace_component.data
        timeScale = np.asarray([t0, t1]) * fm
        return trace_c[int(timeScale[0]):int(timeScale[1])]

    def plot_comp(self):
        if (self.active_component is None) or (int(self.current_x2) == 0):
            pass
        else:
            self.refresh()
            portion = self.select_from_component(self.current_x1, self.current_x2, self.current_fm)
            # canvas signal 1
            timeVector = np.linspace(self.current_x1, self.current_x2, len(portion))
            self.ax = self.figura_signal_1.add_subplot(111)
            # discards the old graph
            self.ax.cla()
            self.ax.plot(timeVector, portion)
            self.canvas_signal_1.draw()
            self.ax1 = self.figura_fft_1.add_subplot(111)
            self.ax1.cla()
            self.ax1.specgram(portion.flatten(), NFFT=64, Fs=self.current_fm, noverlap=32, cmap='jet')
            self.canvas_fft_1.draw()

    def refresh(self):
        self.current_x1 = self.parent().x1
        self.current_x2 = self.parent().x2
        self.label_t0.setText(str(self.current_x1))
        self.label_t1.setText(str(self.current_x2))


class ChildWindowStations(QtGui.QMainWindow, DialogStations.Ui_MainWindow):
    def __init__(self, parent):
        super(ChildWindowStations, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        self.filename_c = ""
        self.current_x1 = self.parent().x1
        self.current_x2 = self.parent().x2

        self.delta_align = None

        self.st1, self.st2, self.fm_s, self.hbf = 0, 0, 0, 0
        self.axis_station = None
        self.axis_specgram = None
        self.station_stream = None
        self.trace_stream = None

        self.load_button.clicked.connect(self.load_data)
        self.pushfirst.clicked.connect(self.plot)
        self.pushButton.clicked.connect(self.refresh)
        self.specgram_button.clicked.connect(self.specgram_plot)
        self.checkBox_trace.clicked.connect(self.enable_params)

        self.set_text_positions(self.current_x1, self.current_x2)

    def set_text_positions(self, t0, t1):
        self.label_start.setText(str(round(t0, 2)))
        self.label_end.setText(str(round(t1, 2)))

    def compute_delta_alignment(self):
        time_main = self.parent().active_trace.stats.starttime
        time_station = self.trace_stream.stats.starttime
        return float(math.ceil(time_station - time_main))

    def process_station(self, stream, fm_s, high_freq):
        aux = stream.copy()
        filtered = aux.filter("highpass", freq=high_freq)
        merged = filtered.merge(method=0, fill_value='interpolate')
        return merged[0]

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Z and self.axis_station:
                self.axis_station.toolbar.zoom()
            elif event.key() == QtCore.Qt.Key_S and self.axis_station:
                self.axis_station.toolbar.pan()
            elif event.key() == QtCore.Qt.Key_U and self.axis_station:
                self.axis_station.toolbar.home()
            elif event.key() == QtCore.Qt.Key_Q:
                self.close()
        else:
            event.ignore()

    def load_data(self):
        self.refresh()
        self.filename_c = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/'))
        self.loaded_station_label.setText(self.filename_c)
        self.station_stream = obspy.read(self.filename_c)

        self.fm_s = self.station_stream[0].stats.sampling_rate

        if self.fm_s == 75.19:
            self.fm_s = 75.0  # montserrat

        self.fm_newstation.setText(str(self.fm_s))
        self.high_pass_fre.setText(str(0.5))

    def plot(self):
        self.refresh()
        if self.parent().active_trace == None or self.filename_c == "":
            pass
        elif self.checkBox_trace.isChecked():
            self.fm_s = float(self.fm_newstation.text())
            self.hbf = float(self.high_pass_fre.text())
            filepath = str(self.loaded_station_label.text())
            self.station_stream = obspy.read(filepath)
            self.st1, self.st2 = 0, 0
            self.clear_canvas()
        else:

            self.trace_stream = self.process_station(self.station_stream, self.fm_s, self.hbf)
            self.delta_align = self.compute_delta_alignment()
            time_Vector = np.linspace(0, len(self.trace_stream) / self.fm_s, num=len(self.trace_stream.data))

            # l3 = "t', %s with %s" % (self.trace_stream.stats.station, self.parent().active_trace.stats.station)

            # create an axis
            self.axis_station = self.figure_signal.add_subplot(111)
            # discards the old graph
            self.axis_station.cla()
            self.axis_station.plot(time_Vector, self.trace_stream.data)

            self.selector_station = RectangleSelector(self.axis_station, self.get_current_pos,
                                                      drawtype='box', useblit=True, button=[1],
                                                      minspanx=5, minspany=5, spancoords='pixels',
                                                      interactive=True)
            self.axis_station.toolbar = NavigationToolbar(self.canvas_signal, self)

            self.axis_station.axvline(self.current_x1, color='darkgreen', linestyle='solid')
            self.axis_station.axvline(self.current_x2, color='green', linestyle='solid')
            self.axis_station.axvline(self.delta_align + self.current_x1, color='orange', linestyle='dotted',
                                      linewidth=2)
            self.canvas_signal.draw()
            gc.collect()

    def get_current_pos(self, eclick, erelease):
        self.st1 = eclick.xdata
        self.st2 = erelease.xdata

    def enable_params(self):
        if self.checkBox_trace.isChecked():
            self.fm_newstation.setEnabled(True)
            self.high_pass_fre.setEnabled(True)
        else:
            self.fm_newstation.setEnabled(False)
            self.high_pass_fre.setEnabled(False)

    def refresh(self):
        self.current_x1 = self.parent().x1
        self.current_x2 = self.parent().x2
        self.set_text_positions(self.current_x1, self.current_x2)
        if self.axis_station:
            [self.axis_station.lines[-1].remove() for x in range(3)]
            self.axis_station.axvline(self.current_x1, color='darkgreen', linestyle='solid')
            self.axis_station.axvline(self.current_x2, color='green', linestyle='solid')
            self.axis_station.axvline(self.delta_align + self.current_x1, color='darkorange', linestyle='dotted',
                                      linewidth=2)
            self.canvas_signal.draw()

    def reset(self, interactive):
        if interactive and self.axis_station is not None:
            mode = self.axis_station.get_navigate_mode()
            if mode == "ZOOM":
                self.axis_station.toolbar.zoom()
            else:
                self.axis_station.toolbar.pan()

    def clear_canvas(self):
        self.figure_specgram.clf()
        self.canvas_specgram.draw()
        self.figure_signal.clf()
        self.canvas_signal.draw()
        self.refresh()

    def specgram_plot(self):
        if self.axis_specgram != None:
            self.axis_specgram.cla()

        if self.st1 <= 0:
            pass
        else:
            valor = np.asarray([self.st1, self.st2]) * self.fm_s
            chunkPlot = self.trace_stream.data[int(valor[0]):int(valor[1])]
            self.axis_specgram = self.figure_specgram.add_subplot(111)
            self.axis_specgram.cla()
            self.axis_specgram.specgram(chunkPlot.flatten(), NFFT=64, Fs=self.fm_s, noverlap=32, cmap='jet')
            self.canvas_specgram.draw()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
