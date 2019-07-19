# -*- coding: utf-8 -*-

"""
Dialog panel to work with other stations from a given network. Functionalities are appended to the main interface.
# WARNING! All changes made in this file will be lost!
Author: A. Bueno
"""

from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        MainWindow.resize(1005, 863)
        # Main widget panel
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        # HOrizontal Layout Panel
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        # Layour for the Loading button
        self.load_button = QtGui.QPushButton(self.centralwidget)
        self.load_button.setObjectName(_fromUtf8("load_button"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.load_button)
        # Loaded station Labels
        self.loaded_station_label = QtGui.QLabel(self.centralwidget)
        self.loaded_station_label.setText(_fromUtf8(""))
        self.loaded_station_label.setObjectName(_fromUtf8("loaded_station_label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.loaded_station_label)
        # Loaded label 4
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        # Label 5 for the checkbox of the trace.
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)

        self.checkBox_trace = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_trace.setText(_fromUtf8(""))
        self.checkBox_trace.setObjectName(_fromUtf8("checkBox_trace"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox_trace)
        # Label for the high frequency filter
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
        self.high_pass_fre = QtGui.QLineEdit(self.centralwidget)
        self.high_pass_fre.setEnabled(False)
        self.high_pass_fre.setObjectName(_fromUtf8("high_pass_fre"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.high_pass_fre)

        # Label for the new frequency on the new station
        self.fm_newstation = QtGui.QLineEdit(self.centralwidget)
        self.fm_newstation.setEnabled(False)
        self.fm_newstation.setObjectName(_fromUtf8("fm_newstation"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.fm_newstation)
        self.horizontalLayout_3.addLayout(self.formLayout_2)

        # Label for the new line
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)

        self.label_end = QtGui.QLabel(self.centralwidget)
        self.label_end.setText(_fromUtf8(""))
        self.label_end.setObjectName(_fromUtf8("label_end"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_end)

        self.label_start = QtGui.QLabel(self.centralwidget)
        self.label_start.setText(_fromUtf8(""))
        self.label_start.setObjectName(_fromUtf8("label_start"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_start)

        self.verticalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_3.addWidget(self.line_2)
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))

        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        # Append both to the main canvas
        self.figure_signal = Figure()
        self.canvas_signal = FigureCanvas(self.figure_signal)
        self.verticalLayout_4.addWidget(self.canvas_signal)

        # Button Layouts
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushfirst = QtGui.QPushButton(self.centralwidget)
        self.pushfirst.setObjectName(_fromUtf8("pushfirst"))
        self.horizontalLayout.addWidget(self.pushfirst)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.figure_specgram = Figure()
        self.canvas_specgram = FigureCanvas(self.figure_specgram)

        self.verticalLayout_4.addWidget(self.canvas_specgram)
        self.specgram_button = QtGui.QPushButton(self.centralwidget)
        self.specgram_button.setObjectName(_fromUtf8("specgram_button"))
        self.verticalLayout_4.addWidget(self.specgram_button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Visualize other stations", None))
        self.load_button.setText(_translate("MainWindow", "Load", None))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Sampling Freq (Hz)</span></p></body></html>", None))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">High_pass Freq (Hz)</span></p></body></html>", None))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Modify Trace Parameters</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Main Window current event</span></p></body></html>", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Starting time </span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">End Time </span></p></body></html>", None))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Z: Zoom </span></p></body></html>", None))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">S: Span</span></p></body></html>", None))
        self.pushfirst.setText(_translate("MainWindow", "Plot Trace", None))
        self.pushButton.setText(_translate("MainWindow", "Refresh", None))
        self.specgram_button.setText(_translate("MainWindow", "Plot Specgram", None))

