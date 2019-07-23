"""PICOSS interface main script.

This script allows the user to run the GUI interface. It is assumed that the seismic data streams has been previously 
processed and stored in an correct format within the data folder (e.g: miniseed), or accessed via data repositories,
such as IRIS. In practice, if the data can be stored in NumPy format, it can be read nby PICOSS. 

PLease, make sure the required modules listed in "requirements.txt" are installed within the working Python environment 
you are interfacing PICOSS with.
"""

# Graphical packages
from PyQt4 import QtGui, QtCore
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# Own packages
from picos_gui import picoss_main
from picos_gui import picoss_func
from picos_gui import gui_functions

from picoss.picos_gui.utils import picos_utils
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
        self.duration = 0
        # String to save
        self.destination_folder = ""

        self.toSave = None

        self.fm = 0  # Sampling Frequency, depends of the active trace
        self.ts = 0  # Time frequency interval. Depends of the trace
        self.highpass_freq = 0.5  # highpass frequency default for the active trace.

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

        # Segmentation table results
        self.segmentation_table = None

        # buttons action definition
        self.btnfft.clicked.connect(self.paint_fft)  # button for the FFT
        self.btnspecgram.clicked.connect(self.paint_spectrogram)  # button for the specgram
        self.buttonGroup.buttonClicked.connect(self.handleButtonClicked)  # button for the labels

        self.submitwindow.clicked.connect(self.submit_current_window)
        self.submittrace.clicked.connect(self.submit_current_trace)

        # ExtraMenus
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


        # Functionalities for the Detection
        self.menu_classification = QtGui.QMenu("&Classification", self)
        self.menu_classification.addAction('&FI', self.showFI)
        self.menuBar().addMenu(self.menu_classification)

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
        webbrowser.open(os.path.join("https://github.com/srsudo/picos/tree/master", "info", "howto"))

    def pop_about(self):
        webbrowser.open(os.path.join("https://github.com/srsudo/picos/tree/master", "info", "about.ipynb"))

    def pop_seismology(self):
        webbrowser.open(os.path.join("https://github.com/srsudo/picos/tree/master", "info", "seismology"))

    def check_plots(self):
        """Function to axis plots."""
        if self.ax is None:
            pass

    """
    Functions to connect with Other Menus
    """

    def showFI(self):
        """
        Function to load the segmented data and compute the results.
        """
        fi_windows = picoss_func.WindowFI(self).show()

    def show_isolated(self):
        """
        Function to load the data from folder whilst updating the parent.
        """
        isolated_menu = picoss_func.WindowLoadFolder(self).show()

    def show_connection(self):
        connection_menu = picoss_func.WindowConnection(self).show()

    def show_components_menu(self):
        component_menu = picoss_func.WindowComponents(self).show()

    def show_other_stations(self):
        """Function to show other stations"""
        stations_window = picoss_func.WindowStations(self).show()

    def load_picking_results(self):
        """Function to load picking results from a previously processed file"""
        stalta = picoss_func.WindowPicklingFile(self).show()

    def show_STALTA(self):
        sta_lta = picoss_func.WindowPickingOnFly(self).show()

    def show_AMPA(self):
        ampa = picoss_func.WindowAmpa(self).show()

    def show_save_menu(self):
        save_menu = picoss_func.WindowSaving(self).show()

    def show_auxiliar_menu(self):
        self.connection_menu = picoss_func.WindowFrequency(self)
        self.connection_menu.show()

    """
    End of Functions to connect with Other Menus
    """

    def process_triggerfile(self, dictionary):
        """
        Function that loads the previously pre-processed STA/LTA file as a dictionary file.
        Notice that in order to make this function to work, the trace must be pre-processed using the CLI,
        specifically, the make_stalta.sh script
        """

        dict_loaded = picos_utils.load_processed_file(dictionary)
        datos = obspy.core.trace.Trace(data=dict_loaded['data'])
        self.active_trace = datos.copy()
        self.stream = obspy.core.stream.Stream(traces=[self.active_trace])
        self.on_of = dict_loaded['on_of']
        self.fm = float(dict_loaded['fm'])  # load the sampling_frequency.
        self.plot_trigger(self.on_of)

    def plot_trigger(self, on_of):
        """
        Function that load the previously pre-processed STA/LTA file as a dictionary file.
        Notice that in order to make this function work, it must be pre-processed using the included CLI,
        specifically, the make_stalta.sh script

        A own dictionary from another picking file, BUT with the following fields are also possible:
            'data' -> (the seismic data we want to process as a Numpy Array)
            'on of' -> an activation vector with triggers on and off times
            'fm' -> the sampling frequency we are working with.

        Args:
            on_of : tuple
                The tuple of activation times for the times

        """

        time_Vector = np.linspace(0, self.active_trace.data.shape[0] / self.fm, num=self.active_trace.data.shape[0])

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
        self.ax.vlines(on_of[:, 0] / self.fm, ymin, ymax, color='r', linewidth=1)
        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()

    def peak_to_peak(self):
        """
        Function to compute the peak_to_peak amplitude in a given trace.
        Returns:
        Numpy
            The absolute value of the peak to peak amplitude
        """

        value = np.asarray([self.x1, self.x2]) * self.fm
        chunkPlot = self.active_trace.data[int(value[0]):int(value[1])]
        return np.abs(np.amax(chunkPlot) - np.amin(chunkPlot))

    def check_overlapping(self, v1, v2):
        """Function to check if the current values are overlapped or not. This function avoid segmentation of overlapped
          events, thus yields robust datasets.
        """
        if float(self.first_ticked) <= v1 <= float(self.last_ticked):
            return True
        elif float(self.first_ticked) <= round(v2, 2) <= float(self.last_ticked):  # change v2 to x2
            return True
        else:
            return False

    def submit_current_window(self):
        """
        This function is used to submit the current window to the segmentation table to store the segmented events
        in the datasets.
        """
        # check which radio button is selected
        if self.current_label == "":
            gui_functions.msg_box("Can not submit if no label is selected", "Please, select one or change window.")
        else:
            # Get the current information from the data
            label = self.current_label
            alumni = self.comments.text()
            slider = self.qualityslider.value()
            start, end = str(round(self.x1, 2)), str(round(self.x2, 2))
            peakAmpl = str(round(self.peak_to_peak(), 2))
            duration = str(abs(float(end) - float(start)))
            # Check if is overlapping or not.
            if self.check_overlapping(round(self.x1, 2), round(self.x2, 2)):
                gui_functions.msg_box("Current window overlap previous one", "Please, move the sliding window.")
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

                # cleaning and redrawing traces.
                new_job = multiprocessing.Process(target=self.clean_figures(), args=())
                new_job.start()

                redraw = multiprocessing.Process(target=self.redraw_trace(), args=())
                redraw.start()
                time.sleep(2)

        gc.collect()

    def handleButtonClicked(self, button):
        """
        Function listener to handle when a button is clicked and modify the member variable to the current value
        Args:
            button: Qt.Button
            The button the user has clicked
        """
        value = button.text().split(" ")[-1]
        self.current_label = value[1:-1]

    def submit_current_trace(self):
        """Function to save the segmented events in a pickle file. Notice that if no segmented events are selected,
           the data can not be saved.
        """
        allRows = self.table_trace.rowCount()

        if self.ax is None or allRows is 0:
            gui_functions.msg_box("No current events are segmented", "Data can not be submitted")
        else:
            segmentation_table = []
            segmentation_table.append((self.start_data, self.end_data))
            for row in xrange(0, allRows):
                start_toSave = str(self.table_trace.item(row, 0).text())
                end_toSave = str(self.table_trace.item(row, 1).text())
                label_toSave = str(self.table_trace.item(row, 2).text())
                peak_toSave = str(self.table_trace.item(row, 3).text())
                duration_toSave = str(self.table_trace.item(row, 4).text())
                slides_toSave = str(self.table_trace.item(row, 5).text())
                alumni_toSave = str(self.table_trace.item(row, 6).text())

                # Created the segmentation table
                new = [start_toSave, end_toSave, label_toSave, peak_toSave, duration_toSave, slides_toSave,
                       alumni_toSave]
                segmentation_table.append(new)

            self.toSave = "%s_%s_%s_%s_%s_%s_%s" % (self.network, self.station, self.channel, self.location,
                                                    self.start_data.year, self.day_of_the_year, self.duration)
            self.segmentation_table = segmentation_table
            # Clean the figures to free memory and allow further plotting.
            self.clean_table()
            self.clean_figures()
            self.clean_points()
            self.figura_traza.clf()
            self.canvas_traza.draw()
            self.show_save_menu()
            gc.collect()

    def clean_table(self):
        """function to clean the segmentation table"""
        self.table_trace.clearContents()
        self.table_trace.setRowCount(0)

    def clean_points(self):
        """function to clean the selected ticked points"""
        self.x1 = 0
        self.x2 = 0
        self.first_ticked = 0
        self.last_ticked = 0

    def clean_canvas(self):
        self.figura_traza.clf()
        self.canvas_traza.draw()

    def clean_figures(self):
        """function to clean the figures and ticked points"""
        self.figura_spectrograma.clf()
        self.figura_fft.clf()
        self.canvas_specgram.draw()
        self.canvas_fft.draw()

    def redraw_trace(self):
        """function to redraw the traces and ticked points"""
        [self.ax.lines[-1].remove() for x in range(2)]
        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()

    def reset_interactive(self):
        """function to reset the interactivity of the interface"""
        mode = self.ax.get_navigate_mode()
        if mode == "ZOOM":
            self.toggle_zoom()
        elif mode == "PAN":
            self.toggle_pan()
        else:
            pass

    def line_select_callback(self, eclick, erelease):
        """
        Function to handle the click of the events, and modify the current traceback in the files
        Args:
            eclick : Qt.Event
                Listener of mouse click of the event
            erelease : Qt.Event
                Release of the mouse click of the event
        """
        # put the previous one to zero, just in case
        self.x1, self.x2 = 0, 0
        self.x1 = eclick.xdata
        self.x2 = erelease.xdata
        new_job = multiprocessing.Process(target=self.clean_figures(), args=())
        new_job.start()

    def toggle_zoom(self):
        """Set Zoom on"""
        if self.ax is not None:
            self.ax.toolbar_trace.zoom()

    def toggle_pan(self):
        """Set Pan on"""
        if self.ax is not None:
            self.ax.toolbar_trace.pan()

    def toggle_view(self):
        """Set main view again"""
        if self.ax is not None:
            self.ax.toolbar_trace.home()

    def plot_from_file(self):
        """function to plot from file the loaded traces"""
        self.stream = obspy.read(self.trace_loaded_filename)
        if self.ax is not None:
            self.clean_figures()
            self.reset_interactive()

        self.prepare_stream()

    def prepare_stream(self, bandpass=None):
        """
        This function handles the data preparation prior to depiction of the seismic trace. Notice that
        local variables are linked here.
        Args:
            bandpass: Python Tuple (float)
                The bandpass filter to apply to the seismic trace.
        """
        # we need to make a copy to preserve original data to avoid Python numeric unstabilities. .
        st = self.stream.copy()

        if bandpass is None:
            filtered = st.filter("highpass", freq=self.highpass_freq)
        else:
            filtered = st.filter("bandpass", freqmin=bandpass[0], freqmax=bandpass[1])

        # Filter the trace as a single one, select the data, and clean it up.
        self.trace_loaded = filtered.merge(method=0)
        self.trace_loaded = self.trace_loaded._cleanup()
        self.active_trace = self.trace_loaded[0]

        if isinstance(self.trace_loaded, obspy.core.stream.Stream):

            self.fm = self.active_trace.stats.sampling_rate

            self.start_data = self.active_trace.stats.starttime
            self.end_data = self.active_trace.stats.endtime
            self.day_of_year = self.start_data.strftime('%j')

            self.duration = int(math.ceil(self.end_data - self.start_data))  # duration in seconds, rounded up
            self.ts = 1 / float(self.fm)

            new_job = multiprocessing.Process(target=self.paint_trace(), args=())
            new_job.start()
            time.sleep(1)

        else:
            raise NotImplementedError

    def plot_from_server(self):
        """Function to plot the loaded trace from the server and link the local variables to the downloaded data.
           It links the local variables and apply a highpass filter automatically to erase background noise.
        """
        filtered = self.trace_loaded.filter("highpass", freq=0.5)

        self.trace_loaded = filtered.merge(method=1)
        self.active_trace = self.trace_loaded[0]

        self.fm = self.active_trace.stats.sampling_rate
        self.ts = 1 / float(self.fm)

        self.start_data = self.active_trace.stats.starttime
        self.end_data = self.active_trace.stats.endtime
        self.day_of_year = self.start_data.strftime('%j')
        self.duration = int(math.ceil(self.end_data - self.start_data))  # duration in seconds, rounded up

        new_job = multiprocessing.Process(target=self.paint_trace(), args=())
        new_job.start()
        time.sleep(1)

    def paint_trace(self):
        """
        Function that paints the trace within the main interface and links the interactivity with the main canvas.
        """

        # init main tick buttons to initial zeroes.
        self.x1, self.x2 = 0, 0

        if self.ax is not None:
            self.ax.cla()

        # get the active trace
        trace = self.active_trace.data
        # Create the time vector in seconds.
        time_Vector = np.linspace(0, len(trace) / self.fm, num=len(trace))
        # create an axis
        self.ax = self.figura_traza.add_subplot(111)
        # discards the old graph
        self.ax.cla()
        self.ax.plot(time_Vector, trace)
        self.ax.toolbar_trace = NavigationToolbar(self.canvas_traza, self)

        # Get the selector
        self.selector = RectangleSelector(self.ax, self.line_select_callback,
                                          drawtype='box', useblit=True, button=[1],
                                          minspanx=5, minspany=5, spancoords='pixels',
                                          interactive=True)

        self.ax.axvline(self.first_ticked, color='green', linestyle='solid')
        self.ax.axvline(self.last_ticked, color='magenta', linestyle='dashed')
        self.canvas_traza.draw()
        gc.collect()

    def paint_spectrogram(self):
        """
        Function that paints the spectrogram within the main interface and links the interactivity with the main canvas.
        """
        if (self.x1 <= 0) or (self.x2 >= len(self.active_trace.data)):
            gui_functions.msg_box("No active window is selected",
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
            self.ax1.specgram(chunkPlot.flatten(), NFFT=128, Fs=self.fm, noverlap=64, cmap='jet')
            self.ax1.set_ylim(0, 30)
            self.canvas_specgram.draw()

    def paint_fft(self):
        """
        This function computes the FFT of the selected signal and plot it on the selected space for it.
        """
        if (self.x1 <= 0) or (self.x2 >= len(self.active_trace.data)):
            gui_functions.msg_box("No active window is selected",
                                  "Please, select one point the trace and drag along the time axis.")
        else:
            if self.ax2 is not None:
                self.ax2.cla()

            signal = self.active_trace.data
            value = np.asarray([self.x1, self.x2]) * self.fm
            selected = signal[int(value[0]):int(value[1])]

            # Check it with the masked arrays on some volcanoes.
            if np.ma.isMaskedArray(selected):
                xi = np.arange(len(selected))
                mask = np.isfinite(selected)
                selected = np.interp(xi, xi[mask], selected[mask])

            y, frq = picos_utils.compute_fft(selected, self.fm)

            self.ax2 = self.figura_fft.add_subplot(111)
            self.ax2.cla()
            self.ax2.set_xlabel('Freq (Hz)')

            if self.loglogaxis.isChecked():
                self.ax2.set_ylabel('log(|Y(freq)|)')
                self.ax2.semilogy(frq[1:], np.abs(y)[1:], 'r')
                self.canvas_fft.draw()
            else:
                self.ax2.set_ylabel('|Y(freq)|')
                self.ax2.plot(frq[1:], abs(y)[1:], 'r')
                self.ax2.set_xlim(0, 20)
                self.canvas_fft.draw()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = Picos()
    ret = app.exec_()
    sys.exit(ret)
