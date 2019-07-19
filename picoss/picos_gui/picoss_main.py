# -*- coding: utf-8 -*-

# PICOSS UI interface createdi'
#
# Created: Sat Jan  6 15:05:58 2019
#      by: Angel Bueno
#
# WARNING! All changes made in this file will be lost!

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
        MainWindow.resize(1588, 905)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.figura_traza = Figure()
        self.canvas_traza = FigureCanvas(self.figura_traza)
        self.verticalLayout_2.addWidget(self.canvas_traza)

        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))

        self.figura_spectrograma = Figure()
        self.canvas_specgram = FigureCanvas(self.figura_spectrograma)
        self.verticalLayout_12.addWidget(self.canvas_specgram)

        self.btnspecgram = QtGui.QPushButton(self.centralwidget)
        self.btnspecgram.setObjectName(_fromUtf8("btnspecgram"))
        self.verticalLayout_12.addWidget(self.btnspecgram)
        self.horizontalLayout_3.addLayout(self.verticalLayout_12)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_3.addWidget(self.line_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.event_chooser = QtGui.QLabel(self.centralwidget)
        self.event_chooser.setObjectName(_fromUtf8("event_chooser"))
        self.verticalLayout.addWidget(self.event_chooser)
        self.regional = QtGui.QRadioButton(self.centralwidget)
        self.regional.setObjectName(_fromUtf8("regional"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.regional)
        self.verticalLayout.addWidget(self.regional)
        self.volcanotectonic = QtGui.QRadioButton(self.centralwidget)
        self.volcanotectonic.setObjectName(_fromUtf8("volcanotectonic"))
        self.buttonGroup.addButton(self.volcanotectonic)
        self.verticalLayout.addWidget(self.volcanotectonic)
        self.longperiod = QtGui.QRadioButton(self.centralwidget)
        self.longperiod.setObjectName(_fromUtf8("longperiod"))
        self.buttonGroup.addButton(self.longperiod)
        self.verticalLayout.addWidget(self.longperiod)
        self.lavaflow = QtGui.QRadioButton(self.centralwidget)
        self.lavaflow.setObjectName(_fromUtf8("lavaflow"))
        self.buttonGroup.addButton(self.lavaflow)
        self.verticalLayout.addWidget(self.lavaflow)
        self.tremor = QtGui.QRadioButton(self.centralwidget)
        self.tremor.setObjectName(_fromUtf8("tremor"))
        self.buttonGroup.addButton(self.tremor)
        self.verticalLayout.addWidget(self.tremor)
        self.rockfalls = QtGui.QRadioButton(self.centralwidget)
        self.rockfalls.setObjectName(_fromUtf8("rockfalls"))
        self.buttonGroup.addButton(self.rockfalls)
        self.verticalLayout.addWidget(self.rockfalls)
        self.explosions = QtGui.QRadioButton(self.centralwidget)
        self.explosions.setObjectName(_fromUtf8("explosions"))
        self.buttonGroup.addButton(self.explosions)
        self.verticalLayout.addWidget(self.explosions)
        self.noise = QtGui.QRadioButton(self.centralwidget)
        self.noise.setObjectName(_fromUtf8("noise"))
        self.buttonGroup.addButton(self.noise)
        self.verticalLayout.addWidget(self.noise)
        self.unknown = QtGui.QRadioButton(self.centralwidget)
        self.unknown.setObjectName(_fromUtf8("unknown"))
        self.buttonGroup.addButton(self.unknown)
        self.verticalLayout.addWidget(self.unknown)
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.label_quality = QtGui.QLabel(self.centralwidget)
        self.label_quality.setObjectName(_fromUtf8("label_quality"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_quality)
        self.qualityslider = QtGui.QSlider(self.centralwidget)
        self.qualityslider.setOrientation(QtCore.Qt.Horizontal)
        self.qualityslider.setRange(1, 5)
        self.qualityslider.setObjectName(_fromUtf8("qualityslider"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.qualityslider)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.comments = QtGui.QLineEdit(self.centralwidget)
        self.comments.setObjectName(_fromUtf8("comments"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.FieldRole, self.comments)
        self.verticalLayout.addLayout(self.formLayout_5)
        self.submitwindow = QtGui.QPushButton(self.centralwidget)
        self.submitwindow.setObjectName(_fromUtf8("submitwindow"))
        self.verticalLayout.addWidget(self.submitwindow)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout_3.addWidget(self.line_3)
        self.verticalLayout_13 = QtGui.QVBoxLayout()
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))

        self.figura_fft = Figure()
        self.canvas_fft = FigureCanvas(self.figura_fft)
        self.verticalLayout_13.addWidget(self.canvas_fft)

        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.loglogaxis = QtGui.QCheckBox(self.centralwidget)
        self.loglogaxis.setObjectName(_fromUtf8("loglogaxis"))
        self.horizontalLayout_4.addWidget(self.loglogaxis)
        self.btnfft = QtGui.QPushButton(self.centralwidget)
        self.btnfft.setObjectName(_fromUtf8("btnfft"))
        self.horizontalLayout_4.addWidget(self.btnfft)
        self.verticalLayout_13.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_13)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.table_trace = QtGui.QTableWidget(self.centralwidget)
        self.table_trace.setObjectName(_fromUtf8("table_trace"))
        self.table_trace.setColumnCount(7)
        self.table_trace.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.table_trace.setHorizontalHeaderItem(6, item)
        self.verticalLayout_8.addWidget(self.table_trace)
        self.verticalLayout_2.addLayout(self.verticalLayout_8)
        self.submittrace = QtGui.QPushButton(self.centralwidget)
        self.submittrace.setObjectName(_fromUtf8("submittrace"))
        self.verticalLayout_2.addWidget(self.submittrace)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PICOSS", None))
        self.btnspecgram.setText(_translate("MainWindow", "Plot Specgram", None))
        self.event_chooser.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Choose one event</span></p></body></html>",
                                              None))
        self.regional.setText(_translate("MainWindow", "Regional Earthquake (REG)", None))
        self.volcanotectonic.setText(_translate("MainWindow", "Volcano Tectonic (VT)", None))
        self.longperiod.setText(_translate("MainWindow", "Long Period (LP)", None))
        self.lavaflow.setText(_translate("MainWindow", "Lava Flow (COL)", None))
        self.tremor.setText(_translate("MainWindow", "Tremor (T)", None))
        self.rockfalls.setText(_translate("MainWindow", "Rockfall (R)", None))
        self.explosions.setText(_translate("MainWindow", "Explosion (EXP)", None))
        self.noise.setText(_translate("MainWindow", "Noise (NOISE)", None))
        self.unknown.setText(_translate("MainWindow", "Unknown (U)", None))
        self.label_quality.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Quality Factor (1-5)</span></p></body></html>",
                                              None))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Comments</span></p></body></html>",
                                      None))
        self.submitwindow.setText(_translate("MainWindow", "Submit Current Window", None))
        self.loglogaxis.setText(_translate("MainWindow", "Log-log axis", None))
        self.btnfft.setText(_translate("MainWindow", "Plot FFT", None))
        item = self.table_trace.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Start", None))
        item = self.table_trace.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "End", None))
        item = self.table_trace.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Label", None))
        item = self.table_trace.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "PeakAmp", None))
        item = self.table_trace.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Duration", None))
        item = self.table_trace.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Q", None))
        item = self.table_trace.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Comments", None))
        self.submittrace.setText(_translate("MainWindow", "Submit ALL Trace ", None))
