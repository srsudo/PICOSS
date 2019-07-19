# -*- coding: utf-8 -*-
"""
Dialog panel to visualize and work with other Components.
Functionalities are appended to the main interface.
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
        MainWindow.resize(993, 804)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.pushButton_3)
        self.label_loaded = QtGui.QLabel(self.centralwidget)
        self.label_loaded.setText(_fromUtf8(""))
        self.label_loaded.setObjectName(_fromUtf8("label_loaded"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_loaded)
        self.label_text_start = QtGui.QLabel(self.centralwidget)
        self.label_text_start.setObjectName(_fromUtf8("label_text_start"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_text_start)
        self.label_t0 = QtGui.QLabel(self.centralwidget)
        self.label_t0.setText(_fromUtf8(""))
        self.label_t0.setObjectName(_fromUtf8("label_t0"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_t0)
        self.label_text_end = QtGui.QLabel(self.centralwidget)
        self.label_text_end.setObjectName(_fromUtf8("label_text_end"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_text_end)
        self.label_t1 = QtGui.QLabel(self.centralwidget)
        self.label_t1.setText(_fromUtf8(""))
        self.label_t1.setObjectName(_fromUtf8("label_t1"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_t1)
        self.verticalLayout.addLayout(self.formLayout_2)

        # Figure panel for the main document
        self.figura_signal_1 = Figure()
        self.canvas_signal_1 = FigureCanvas(self.figura_signal_1)
        self.verticalLayout.addWidget(self.canvas_signal_1)

        # Figure panel for the FFT
        self.figura_fft_1 = Figure()
        self.canvas_fft_1 = FigureCanvas(self.figura_fft_1)
        self.verticalLayout.addWidget(self.canvas_fft_1)

        # Figure panel for the button
        self.pushfirst = QtGui.QPushButton(self.centralwidget)
        self.pushfirst.setObjectName(_fromUtf8("pushfirst"))
        self.verticalLayout.addWidget(self.pushfirst)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Visualize other components", None))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Other components to help in the visualization</span></p></body></html>", None))
        self.pushButton_3.setText(_translate("MainWindow", "Load", None))
        self.label_text_start.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">start-time</span></p></body></html>", None))
        self.label_text_end.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">end label</span></p></body></html>", None))
        self.pushfirst.setText(_translate("MainWindow", "Plot", None))

