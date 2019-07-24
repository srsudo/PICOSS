import sys
sys.path.append('..')
import gc
import numpy as np
import obspy
import math
import multiprocessing
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
from menus import DialogTrigger
from menus import DialogAmpa
from menus import DialogFI

import gui_functions
import utils

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
            self.parent().plot_trigger()
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
            self.parent().clean_figures()
            self.parent().clean_points()
            self.parent().clean_canvas()
            self.parent().process_triggerfile(str(self.filename))
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

    def load_pfile(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'picking_data/'))
        self.label_filename_2.setText(self.filename)
        self.autocomplete(self.filename)


class WindowSaving(QtGui.QMainWindow, DialogSave.Ui_MainWindow):
    """
    Function that handles the stations required for saving the data in multiple formats.
    As a default "segmented_data" is given as the default folder, but users cans elect and move within their own data
    structure. Alternatively, other data files can be loaded within the interface.
    """
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
        """Function to browse the folder structure to save a specific file"""
        destination_folder = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Folder"))
        self.label_4.setText(destination_folder)

    def cancel(self):
        """Close the interface"""
        self.close()
        gc.collect()

    def save_data(self):
        """save the data within the selected folder"""
        destination_folder = str(self.label_4.text())
        self.toSave = str(self.filename.text())
        data_format = str(self.comboBox.currentText())
        gui_functions.save_segmentation_table(destination_folder, self.toSave, data_format, self.segmentation_table)
        self.close()


class WindowPickingOnFly(QtGui.QMainWindow, DialogTrigger.Ui_MainWindow):
    """
    Function that handles the computation of STA/LTA files, and interfaces with the main GUI with the triggering and
    plotting functionalities. Alternatively, other data files can be loaded within the interface.
    """
    def __init__(self, parent):
        super(WindowPickingOnFly, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow

        self.buttonComputePlot.clicked.connect(self.compute_plot)
        self.buttonCancel.clicked.connect(self.cancel)
        self.label_loaded.setText(str(self.parent().trace_loaded_filename))

    def compute_plot(self):
        # get the data from the parent and compute
        new_job = multiprocessing.Process(target=self.parent().clean_figures(), args=())
        new_job_main = multiprocessing.Process(target=self.parent().clean_canvas(), args=())
        new_job.start()
        new_job_main.start()
        # Get the info and compute
        kind, nlta, nsta, tgon, toff = self.get_info()

        trace = self.parent().active_trace.copy()  # we copy the data to avoid numerical errors.
        data = utils.picos_utils.check_masked_array(trace.data)

        cft, on_of = utils.picos_utils.compute_sta_lta(data, self.parent().fm,  kind, nlta=nlta,
                                                       nsta=nsta, trig_on=tgon, trig_off=toff)

        self.parent().plot_trigger(on_of)
        self.close()
        gc.collect()

    def cancel(self):
        """close the window"""
        self.close()
        gc.collect()

    def get_info(self):
        """
        Get the information required for the STA/LTA algorithm, along with the type of STA/LTA we want to run
        Returns:
            kind : str
                The type of filter we want to have
            nlta : float
                The length of the LTA window (s)
            nsta : float
                The length of the STA window (s)
            tgon : float
                The trigger "on" to consider an activation
            toff: float
                The trigger "off to deactivate the trigger
        """
        nlta = float(self.spin_lta.value())
        nsta = float(self.spin_sta.value())
        tgon = float(self.trigg_on.value())
        toff = float(self.trigg_of.value())
        kind = str(self.comboTrigger.currentText()).split(" ")[0]

        return kind, nlta, nsta, tgon, toff


class WindowAmpa(QtGui.QMainWindow, DialogAmpa.Ui_MainWindow):
    """
    Function that handles the computation of STA/LTA files, and interfaces with the main GUI with the triggering and
    plotting functionalities. Alternatively, other data files can be loaded within the interface.
    """
    def __init__(self, parent):
        super(WindowAmpa, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow

        self.buttonComputePlot.clicked.connect(self.compute_ampa)
        self.buttonCancel.clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.add_filter)
        self.label_loaded.setText(str(self.parent().trace_loaded_filename))


    def compute_ampa(self):
        # get the data from the parent and compute
        new_job = multiprocessing.Process(target=self.parent().clean_figures(), args=())
        new_job_main = multiprocessing.Process(target=self.parent().clean_canvas(), args=())
        new_job.start()
        new_job_main.start()
        self.compute()


    def cancel(self):
        """close the window"""
        self.close()
        gc.collect()

    def get_info_ampa(self):
        """
        Function that computes the information required for AMPA
        Returns:
            window : float
                Initial frequency for AMPA
            overlap : float
                End frequency for AMPA
            noise : float
                The bandwith with the
            uvalue : float
                Impulssivenes of the filter response
        """

        window = float(self.windowAnalysis.value())
        overlap = float(self.percOverlap.value())
        noise = float(self.spinBox.value())
        uvalue = float(self.uValue.value())

        return window, overlap, noise, uvalue

    def get_info_filters(self):
        """
        Function that gets the info of the filters
        Returns:
            initfreq : float
                Initial frequency for AMPA
            endfreq : float
                End frequency for AMPA
            bandwidth : float
                The bandwith with the
            beta : float
                Impulssivenes of the filter response
            L_filters : list
                The list of filters we will use
        """
        initfreq = float(self.initialfreq.value())
        endfreq = float(self.endfreq.value())
        bandwidth = float(self.bandWidth.value())
        beta = float(self.lcoefficient.value())
        L_filters = []

        # we recover the correspondent value. CHanges this part in a future
        for row in xrange(0, self.tableWidget.rowCount()):
            value = str(self.tableWidget.item(row, 0).text())
            if gui_functions.check_digits(value):
                L_filters.append(value)

        return [initfreq, endfreq, bandwidth, beta, L_filters]

    def compute(self):
        """Function to link and compute the AMPA method"""
        [window, overlap, noise, uvalue] = self.get_info_ampa()
        [initfreq, endfreq, bandwidth, beta, L_filters] = self.get_info_filters()

        trace = self.parent().active_trace.copy()  # we copy the data to avoid numerical errors.
        data = utils.picos_utils.check_masked_array(trace.data)

        on_of = utils.picos_utils.compute_ampa(data, self.parent().fm, window, bandwidth, initfreq, endfreq, overlap,
                                               noise, uvalue, beta, L_filters)

        self.parent().plot_trigger(on_of)
        del trace, data
        self.close()

    def update_rows(self):
        numrows = self.tableWidget.rowCount()
        new_headers = ["Filter %s" % x for x in xrange(1, numrows)]
        self.tableWidget.setVerticalHeaderLabels(new_headers)

    def add_filter(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        numrows = self.tableWidget.rowCount()
        self.tableWidget.setItem(numrows -1, 0, QtGui.QTableWidgetItem("Write value"))
        self.tableWidget.item(numrows-1, 0).setBackground(QtCore.Qt.green)
        self.update_rows()


class WindowFI(QtGui.QMainWindow, DialogFI.Ui_MainWindow):
    """
    Function that handles the computation of the Frequency Index Classification from the segmented files. Alternatively,
     other data files can be loaded within the interface.
    """
    def __init__(self, parent):
        super(WindowFI, self).__init__(parent)
        self.setupUi(self)
        self.parentWindow = picoss_main.Ui_MainWindow

        # high and low pass buttons.
        self.buttonCancel.clicked.connect(self.cancel)
        self.buttonLoad.clicked.connect(self.load_file_segmentation)
        self.buttonLoadTrace.clicked.connect(self.load_file_trace)

        self.radioButtonMX.clicked.connect(self.enable_hybrids)
        self.buttonComputeSave.clicked.connect(self.compute_classification)
        self.loadedMaintrace.setText(self.parent().trace_loaded_filename)

        self.trace = None
        self.filename = None

    def compute_classification(self):
        """
        Functions that computes the
        Returns:
        """
        destination_folder = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Folder"))

        mu_l = -float(self.mu1.value())
        mu_h = float(self.mu2.value())
        mu_r = float(self.mu3.value())
        hyb = self.get_hybrids()

        t_user = 25.0

        slider = float(self.sliderFrequency.value())
        filename_seg = str(self.loadedsegmentation.text())
        filename_trace = str(self.loadedMaintrace.text())

        if slider < 2:
            gui_functions.msg_box("Frequency Index requires broader frequency span", "Please, select Threshold values")
        elif filename_trace == '' or filename_seg is '':
            gui_functions.msg_box("The segmentation table and/or loaded files are required", "Please, load both files")
        else:
            # Obtain the main trace
            self.trace, fm = self.process_data(filename_trace)
            segmentation_times = utils.picos_utils.process_segmentation_table(filename_seg)
            candidates_segmented, durations = np.asarray(utils.picos_utils.extract_signals(self.trace.data, fm, segmentation_times))
            ratios = utils.picos_utils.evaluate_candidates(candidates_segmented, slider, fm)
            labels = utils.picos_utils.evaluate_ratios(ratios, durations, thr_dur=t_user, mu_low=mu_l, mu_high=mu_h, mu_rock=mu_r, mixed=hyb)

            #
            data_toSave = {"segmentation_times": segmentation_times, "labels":labels}
            toSave = "%s_FI.p" % filename_trace.split("/")[-1]

            utils.picos_utils.save_pickle(destination_folder, toSave, data_toSave)
            gc.collect()
            self.close()

    def cancel(self):
        """close the window"""
        self.close()
        gc.collect()

    def process_data(self, filename_trace):
        """function to process the data or copy from the main trace"""
        try:
            trace, fm = utils.picos_utils.process_trace(filename_trace, bandpass=[0.5, 20.0])

        except:
            trace, fm = self.parent().active_trace, self.parent().fm

        return trace, fm

    def load_file_segmentation(self):
        """function to load the segmentation file"""

        self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'segmented_data/'))
        self.loadedsegmentation.setText(self.filename)

    def load_file_trace(self):
        self.loadedMaintrace.setText(str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'data/')))

    def empty_filed(self, val1, val2):
        """
        Function that checks if the hybrid low and hybrid high are checked or not, and if they are number.
        Args:

            val1 : str:
                The first value to check
            val2 : str
                The second value to check
        Returns:
        True if any of the fields are empty, or not nobers
        """

        cond1 = gui_functions.check_emptiness(val1) and gui_functions.check_emptiness(val2)
        cond2 = gui_functions.check_digits(val1) and gui_functions.check_digits(val2)

        return cond1 and cond2

    def get_hybrids(self):
        """
        Function get the information of the hybrids
        """
        mu_hybrid_l = str(self.hybridlow.text())
        mu_hybrid_h = str(self.hybridhigh.text())
        L = None
        if self.radioButtonMX.isChecked() and self.empty_filed(mu_hybrid_l, mu_hybrid_h):
            L = [float(mu_hybrid_l), (mu_hybrid_h)]
        return L

    def enable_hybrids(self):
        """Function to enable the hybrids frequency classification"""
        if self.radioButtonMX.isChecked():
            self.hybridhigh.setEnabled(True)
            self.hybridlow.setEnabled(True)
        else:
            self.hybridhigh.setEnabled(False)
            self.hybridlow.setEnabled(False)