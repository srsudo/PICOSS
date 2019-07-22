# -*- coding: utf-8 -*-

"""
Form implementation created for the Connection with the Remote Repositories
It includes a mwe of the required fields to send a connection.
@author: A. Bueno
"""

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(282, 398)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.ip_c = QtGui.QLineEdit(self.centralwidget)
        self.ip_c.setObjectName(_fromUtf8("ip_c"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.ip_c)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.port_c = QtGui.QLineEdit(self.centralwidget)
        self.port_c.setObjectName(_fromUtf8("port_c"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.port_c)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.comboServers = QtGui.QComboBox(self.centralwidget)
        self.comboServers.setObjectName(_fromUtf8("comboServers"))
        self.comboServers.addItem(_fromUtf8(""))
        self.comboServers.addItem(_fromUtf8(""))
        self.comboServers.addItem(_fromUtf8(""))
        self.comboServers.addItem(_fromUtf8(""))
        self.comboServers.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboServers)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.line)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_7)
        self.network_c = QtGui.QLineEdit(self.centralwidget)
        self.network_c.setObjectName(_fromUtf8("network_c"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.network_c)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_8)
        self.station_c = QtGui.QLineEdit(self.centralwidget)
        self.station_c.setObjectName(_fromUtf8("station_c"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.station_c)
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_9)
        self.channel_c = QtGui.QLineEdit(self.centralwidget)
        self.channel_c.setObjectName(_fromUtf8("channel_c"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.channel_c)
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_10)
        self.location_c = QtGui.QLineEdit(self.centralwidget)
        self.location_c.setObjectName(_fromUtf8("location_c"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.location_c)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.SpanningRole, self.line_2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_3)
        self.startTime = QtGui.QDateTimeEdit(self.centralwidget)
        self.startTime.setObjectName(_fromUtf8("startTime"))
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.FieldRole, self.startTime)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_5)
        self.endTime = QtGui.QDateTimeEdit(self.centralwidget)
        self.endTime.setObjectName(_fromUtf8("endTime"))
        self.formLayout_2.setWidget(11, QtGui.QFormLayout.FieldRole, self.endTime)
        self.label_filename_2 = QtGui.QLabel(self.centralwidget)
        self.label_filename_2.setText(_fromUtf8(""))
        self.label_filename_2.setObjectName(_fromUtf8("label_filename_2"))
        self.formLayout_2.setWidget(12, QtGui.QFormLayout.FieldRole, self.label_filename_2)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.requestbutton = QtGui.QPushButton(self.centralwidget)
        self.requestbutton.setObjectName(_fromUtf8("requestbutton"))
        self.verticalLayout.addWidget(self.requestbutton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Request From Server", None))
        self.label.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">IP (or repository)</span></p></body></html>", None))
        self.label_2.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Port</span></p></body></html>", None))
        self.label_6.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Client</span></p></body></html>", None))
        self.comboServers.setItemText(0, _translate("Request From Server", "Earthworm", None))
        self.comboServers.setItemText(1, _translate("Request From Server", "Seedlink", None))
        self.comboServers.setItemText(2, _translate("Request From Server", "FDSN", None))
        self.comboServers.setItemText(3, _translate("Request From Server", "arclink", None))
        self.comboServers.setItemText(4, _translate("Request From Server", "IRIS", None))
        self.label_7.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Network</span></p></body></html>", None))
        self.label_8.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Station  </span></p></body></html>", None))
        self.label_9.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Channel</span></p></body></html>", None))
        self.label_10.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Location</span></p></body></html>", None))
        self.label_3.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Starting Time</span></p></body></html>", None))
        self.label_5.setText(_translate("Request From Server", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Ending Time</span></p></body></html>", None))
        self.requestbutton.setText(_translate("Request From Server", "Request and Plot", None))

