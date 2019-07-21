import sys
sys.path.append('..')
import gc
import numpy as np
import obspy
import math
from obspy import UTCDateTime

# Graphical Packages
from PyQt4 import QtGui, QtCore
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# Main PICOSS modules
import picoss_main
from menus import DialogFolder
from menus import DialogConnection
from menus import DialogComponents
from menus import DialogStations
from menus import DialogFiltering
from menus import DialogPickingFile
from menus import DialogSave

import gui_functions


class WindowLoadFolder(QtGui.QMainWindow, DialogFolder.Ui_MainWindow):
    """ This class handles the data loading from an input folder.
    """
    def __init__(self, parent):
        super(WindowLoadFolder, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        # Here, we should add the listener
        self.pushButton_4.clicked.connect(self.get_info)
        self.pushButton_3.clicked.connect(self.load_isolated)
        self.filename = None
        self.job = None
        self.sta_lta = False

    def get_info(self):
        """Function to get the trace info"""
        if self.filename is None:
            self.parent().msg_box("Can not submit without a file!", "Choose one file")
        elif self.filename is not None and self.sta_lta:
            self.update_parent_fromText()
            self.parent().plot_stalta()
            self.close()

        else:
            # In case the file is chosen, we get the attributes we want
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


class WindowConnection(QtGui.QMainWindow, DialogConnection.Ui_MainWindow):
    """
    This class handles the connection with the data repositories and send back the data to the main interface.
    """
    def __init__(self, parent):
        super(WindowConnection, self).__init__(parent)
        self.setupUi(self)
        self.requestbutton.clicked.connect(self.requestdata)
        self.cnt = None

    def select_client(self, client):
        """
        Function that creates the client for connectivity according to user's input, and link with the users variables.
        Args:
            client: str
            The type of client we want to connect with.
        """
        if client == 'Earthworm':
            from obspy.clients.earthworm import Client as EClient
            self.cnt = EClient(self.ip_address, int(self.port))
        elif client == 'Seedlink':
            from obspy.clients.seedlink import Client as SClient
            self.cnt = SClient(self.ip_address, int(self.port))
        elif client == 'FDSN':
            from obspy.clients.fdsn import Client as FClient
            self.cnt = FClient(self.ip_address, self.port)
        elif client == 'arclink':
            from obspy.clients.arclink import Client as AClient
            self.cnt = AClient(self.ip_address, int(self.port))
        else:
            from obspy.clients.iris import Client as IClient
            self.cnt = IClient("IRIS")

    def requestdata(self):
        """ Native function to request data from the clients."""
        self.ip_address = self.ip_c.text()
        self.port = int(self.port_c.text())

        if self.ip_address == '' or self.port == '':
            gui_functions.msg_box("IP address or port seems empty", "Please, enter data correctly!")

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

        # a test trace below for test. Remove on final versions.
        # st = "9702-10-1441-50S.MVO_18_1" #this is only from test!!
        self.parent().trace_loaded = st
        self.parent().stream = st
        self.close()
        gc.collect()
        self.parent().plot_from_server()


class WindowComponents(QtGui.QMainWindow, DialogComponents.Ui_MainWindow):
    def __init__(self, parent):
        super(WindowComponents, self).__init__(parent)
        self.setupUi(self)

        # Define the parent window
        self.parentWindow = picoss_main.Ui_MainWindow

        # Define the push buttons we want to use.
        self.pushButton_3.clicked.connect(self.load_data)
        self.pushfirst.clicked.connect(self.plot_comp)

        # Define current x1 and x2, as zero.
        self.current_x1, self.current_x2 = self.parent().x1, self.parent().x2
        self.current_fm = self.parent().fm

        # Define the labels for the text.
        self.label_t0.setText(str(self.current_x1))
        self.label_t1.setText(str(self.current_x2))

        # Define the active components.
        self.active_component = None
        self.trace_component = None
        self.filename_c = None

    def load_data(self):
        """
        Function to load the component data from a given, and link the loaded data, with the active component.
        """
        self.refresh()
        self.filename_c = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/'))
        self.label_loaded.setText(self.filename_c)
        self.active_component = obspy.read(self.filename_c)
        self.process_component()

    def process_component(self):
        """
        Function to process, by filtering and merging, a loaded component of the trace.
        Returns:
            trace component with the numpy array loaded.
        """
        filtered = self.active_component.filter("highpass", freq=self.parent().highpass_freq)
        self.active_component = filtered.merge(method=0, fill_value='interpolate')
        self.trace_component = self.active_component[0]
        return self.trace_component

    def select_from_component(self, t0, t1, fm):
        """
        Function that select a specific time scale in a given trace
        Args:
            t0 : int
                The starting time of the trace
            t1 : int
                The end time of the trace
            fm : float
                The sampling frequency of the trace

        Returns :
        Numpy
            The selected part of the trace.
        """
        trace_c = self.trace_component.data
        timeScale = np.asarray([t0, t1]) * fm
        return trace_c[int(timeScale[0]):int(timeScale[1])]

    def plot_comp(self):
        """ Function to plot the component, similar to the one in run_picos.py
            Additional functions and auxiliary code is appended via run_picos.py
        """
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


class WindowStations(QtGui.QMainWindow, DialogStations.Ui_MainWindow):
    """
    Function that loads another station to visualize multi-components separately.
    By loading another station in the program, we can see attenuation and similar
    phenomena. Alternatively, other data files can be loaded within the interface.
    """
    def __init__(self, parent):
        super(WindowStations, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        self.filename_c = ""

        # This gets the position in the parent node to infer (approximately) where we are in the new one

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
        """
        Function to process the streams for any given station.
        Any missing values are interpolated and filled with zeroes.
        Args:
            stream : Obspy.Stream object
                The seismic data stream we want to process.
            fm_s : float
                The sampling frequency of the stream
            high_freq : float
                The default high frequency we want to work with

        Returns:
            numpy array containing the full trace.
        """
        aux = stream.copy()  # to avoid modification of the trace.
        filtered = aux.filter("highpass", freq=high_freq)
        merged = filtered.merge(method=0, fill_value='interpolate')
        return merged[0]

    def keyPressEvent(self, event):
        """
        Handle the click of events. If not clicked within the available options, it just get ignored.
        Args:
            event: QtGui.QKeyEvent
            The type of event that has been clicked and selected.
        """
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
        """Load the data from a folder"""
        self.refresh()
        self.filename_c = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/'))
        self.loaded_station_label.setText(self.filename_c)
        self.station_stream = obspy.read(self.filename_c)
        self.fm_s = self.station_stream[0].stats.sampling_rate
        self.fm_newstation.setText(str(self.fm_s))
        self.high_pass_fre.setText(str(0.5))

    def plot(self):
        self.refresh()
        if self.parent().active_trace is None or self.filename_c == "":
            pass
        elif self.checkBox_trace.isChecked():
            # get the filepath
            filepath = str(self.loaded_station_label.text())
            self.fm_s = float(self.fm_newstation.text())
            self.hbf = float(self.high_pass_fre.text())
            self.station_stream = obspy.read(filepath)
            self.st1, self.st2 = 0, 0
            self.clear_canvas()

        else:

            self.trace_stream = self.process_station(self.station_stream, self.fm_s, self.hbf)
            self.delta_align = self.compute_delta_alignment()
            time_Vector = np.linspace(0, len(self.trace_stream) / self.fm_s, num=len(self.trace_stream.data))

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
        """Function to reset the controls and the main interface."""
        if interactive and self.axis_station is not None:
            mode = self.axis_station.get_navigate_mode()
            if mode == "ZOOM":
                self.axis_station.toolbar.zoom()
            else:
                self.axis_station.toolbar.pan()

    def clear_canvas(self):
        "clear the canvas and refres the variables."
        self.figure_specgram.clf()
        self.canvas_specgram.draw()
        self.figure_signal.clf()
        self.canvas_signal.draw()
        self.refresh()

    def specgram_plot(self):
        """Function to plot the spectrogram of the selected event."""
        if self.axis_specgram is not None:
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


class WindowFrequency(QtGui.QMainWindow, DialogFiltering.Ui_MainWindow):
    def __init__(self, parent):
        super(WindowFrequency, self).__init__(parent)
        self.setupUi(self)
        # get the sampling frequency of the parent node.
        self.new_fm.setText(str(self.parent().fm))
        # get the frequency of the default high frequency filter.
        self.highpass_new.setText(str(self.parent().highpass_freq))
        self.replot.clicked.connect(self.plot)
        # get the name of the loaded trace.
        self.filename_current_trace.setText(self.parent().trace_loaded_filename)
        # high and low pass buttons.
        self.button_bandpass.clicked.connect(self.enable_bandpass)
        self.button_highpass.clicked.connect(self.enable_highpass)

    def check_param(self, param):
        """Function to check if the input field is empty or not."""
        if gui_functions.check_digits(param) and gui_functions.check_emptiness(param):
            return True
        else:
            return False

    def enable_bandpass(self):
        """Function to enable bandpass filtering to our data."""
        self.bp_highfreq.setEnabled(True)
        self.bp_downfreq.setEnabled(True)
        self.highpass_new.setEnabled(False)

    def enable_highpass(self):
        """Function to enable highpass filtering to our data."""
        self.highpass_new.setEnabled(True)
        self.bp_highfreq.setEnabled(False)
        self.bp_downfreq.setEnabled(False)

    def plot(self):
        """Function to plot the frequency options, and re-draw with the new interface options"""
        self.parent().reset_interactive()
        fm = str(self.new_fm.text())
        freq_but = str(self.highpass_new.text())

        # Check type of filters and apply to the ORIGINAL data.
        if self.button_bandpass.isChecked() and self.check_param(fm):
            freq_high = str(self.bp_highfreq.text())
            freq_low = str(self.bp_downfreq.text())
            if (self.check_param(freq_high) and self.check_param(freq_low)) \
                    and (float(freq_high) > float(freq_low)):

                # clean stuff parent node and re-draw abck
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


class WindowPicklingFile(QtGui.QMainWindow, DialogPickingFile.Ui_MainWindow):
    def __init__(self, parent):
        super(WindowPicklingFile, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        # Here, we should add the listener
        self.pushButton_4.clicked.connect(self.get_info)
        self.pushButton_3.clicked.connect(self.load_pfile)
        self.filename = None
        self.sta_lta = False

    def get_info(self):

        if self.filename is None:
            self.parent().msg_box("Can not plot without preprocessed file!", "Choose one preprocessed file")
        elif self.filename is not None:
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

    def load_pfile(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'picking_data/'))
        self.label_filename_2.setText(self.filename)
        self.autocomplete(self.filename)


class WindowSaving(QtGui.QMainWindow, DialogSave.Ui_MainWindow):

    def __init__(self, parent):
        super(WindowSaving, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow
        # Here, we should add the listener
        self.segmentation_table = self.parent().segmentation_table
        self.toSave = None
        self.filename.setText(str(self.parent().toSave))
        self.label_4.setText("segmented_data/")
        # Here, we should add the listener
        self.pushButton.clicked.connect(self.browse)
        self.buttonCancel.clicked.connect(self.cancel)
        self.buttonSave.clicked.connect(self.save_data)


    def browse(self):
        destination_folder = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Folder"))
        self.label_4.setText(destination_folder)

    def cancel(self):
        self.close()
        gc.collect()

    def save_data(self):
        destination_folder = str(self.label_4.text())
        self.toSave = str(self.filename.text())
        data_format = str(self.comboBox.currentText())
        gui_functions.save_segmentation_table(destination_folder, self.toSave, data_format, self.segmentation_table)
        self.close()
