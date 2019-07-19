import sys
sys.path.append('..')
from PyQt4 import QtGui

# Main PICOSS modules
import picoss_main
from menus import DialogFolder
from menus import DialogConnection
import gui_functions
from obspy import UTCDateTime
import gc


class WindowLoadFolder(QtGui.QMainWindow, DialogFolder.Ui_MainWindow):
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
            from obspy.clients.fdsn import Client as FClient
            self.cnt = FClient(self.ip_address, self.port)
        elif client == 'arclink':
            from obspy.clients.arclink import Client as AClient
            self.cnt = AClient(self.ip_address, int(self.port))
        else:
            from obspy.clients.iris import Client as IClient
            self.cnt = IClient("IRIS")

    def requestdata(self):

        self.ip_address = self.ip_c.text()
        self.port = int(self.port_c.text())

        if self.ip_address == '' or self.port == '':
            gui_functions.msg_box("IP address or port seems empty", "Please, enter data correctly!")
        else:


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