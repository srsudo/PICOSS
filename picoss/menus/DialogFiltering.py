# -*- coding: utf-8 -*-

"""
Dialog panel to visualize and work with the filtering and frequency options
Functionalities are appended to the main interface.
# WARNING! All changes made in this file will be lost!
Author: A. Bueno
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
        MainWindow.resize(600, 267)

        # Main panel
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        # Layout configuration
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        # Labels required
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        # Sampling frequency
        self.new_fm = QtGui.QLineEdit(self.centralwidget)
        self.new_fm.setObjectName(_fromUtf8("new_fm"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.new_fm)
        # Label required for the samplin frequency
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)

        self.button_highpass = QtGui.QRadioButton(self.centralwidget)
        self.button_highpass.setText(_fromUtf8(""))
        self.button_highpass.setObjectName(_fromUtf8("button_highpass"))
        self.buttonGroupFilters = QtGui.QButtonGroup(MainWindow)
        self.buttonGroupFilters.setObjectName(_fromUtf8("buttonGroupFilters"))
        self.buttonGroupFilters.addButton(self.button_highpass)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.button_highpass)

        # Main button required for the highpass functionality
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.highpass_new = QtGui.QLineEdit(self.centralwidget)
        self.highpass_new.setObjectName(_fromUtf8("highpass_new"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.highpass_new)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        # Panel to show the filename of the current trace
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.filename_current_trace = QtGui.QLabel(self.centralwidget)
        self.filename_current_trace.setText(_fromUtf8(""))
        self.filename_current_trace.setObjectName(_fromUtf8("filename_current_trace"))
        # Bandpass lay outs
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.filename_current_trace)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.line)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.button_bandpass = QtGui.QRadioButton(self.centralwidget)
        self.button_bandpass.setEnabled(True)
        self.button_bandpass.setText(_fromUtf8(""))
        self.button_bandpass.setObjectName(_fromUtf8("button_bandpass"))
        self.buttonGroupFilters.addButton(self.button_bandpass)
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.button_bandpass)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        # Bandpass High Frequency.
        self.bp_highfreq = QtGui.QLineEdit(self.centralwidget)
        self.bp_highfreq.setEnabled(False)
        self.bp_highfreq.setObjectName(_fromUtf8("bp_highfreq"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.bp_highfreq)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.replot = QtGui.QPushButton(self.centralwidget)
        self.replot.setObjectName(_fromUtf8("replot"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.replot)
        self.bp_downfreq = QtGui.QLineEdit(self.centralwidget)
        self.bp_downfreq.setEnabled(False)
        # Bandpass Low Frequency
        self.bp_downfreq.setObjectName(_fromUtf8("bp_downfreq"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.bp_downfreq)
        self.verticalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Frequency and Filtering", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Sampling Frequency (Hz)</span></p></body></html>", None))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Highpass-filter</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Filter Corner Frequency</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Loaded Trace</span></p></body></html>", None))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">BandPass Filter</span></p></body></html>", None))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Upper frequency (Hz)</span></p></body></html>", None))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Down Frequency (Hz)</span></p></body></html>", None))
        self.replot.setText(_translate("MainWindow", "Plot ", None))

