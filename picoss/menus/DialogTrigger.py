# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_stalta.ui'
#
# Created: Sat Jul 20 23:49:58 2019
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

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
        MainWindow.resize(637, 387)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_loaded = QtGui.QLabel(self.centralwidget)
        self.label_loaded.setText(_fromUtf8(""))
        self.label_loaded.setObjectName(_fromUtf8("label_loaded"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_loaded)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboTrigger = QtGui.QComboBox(self.centralwidget)
        self.comboTrigger.setObjectName(_fromUtf8("comboTrigger"))
        self.comboTrigger.addItem(_fromUtf8(""))
        self.comboTrigger.addItem(_fromUtf8(""))
        self.comboTrigger.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboTrigger)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_2.addWidget(self.line_2)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_2.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.spin_lta = QtGui.QDoubleSpinBox(self.centralwidget)
        self.spin_lta.setMaximum(59.0)
        self.spin_lta.setSingleStep(0.0)
        self.spin_lta.setProperty("value", 10.0)
        self.spin_lta.setObjectName(_fromUtf8("spin_lta"))
        self.gridLayout.addWidget(self.spin_lta, 0, 1, 1, 1)
        self.spin_sta = QtGui.QDoubleSpinBox(self.centralwidget)
        self.spin_sta.setMaximum(59.0)
        self.spin_sta.setProperty("value", 5.0)
        self.spin_sta.setObjectName(_fromUtf8("spin_sta"))
        self.gridLayout.addWidget(self.spin_sta, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.trigg_on = QtGui.QDoubleSpinBox(self.centralwidget)
        self.trigg_on.setMaximum(30.0)
        self.trigg_on.setSingleStep(0.1)
        self.trigg_on.setProperty("value", 1.2)
        self.trigg_on.setObjectName(_fromUtf8("trigg_on"))
        self.gridLayout.addWidget(self.trigg_on, 0, 3, 1, 1)
        self.trigg_of = QtGui.QDoubleSpinBox(self.centralwidget)
        self.trigg_of.setMaximum(30.0)
        self.trigg_of.setSingleStep(0.1)
        self.trigg_of.setProperty("value", 0.5)
        self.trigg_of.setObjectName(_fromUtf8("trigg_of"))
        self.gridLayout.addWidget(self.trigg_of, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonCancel = QtGui.QPushButton(self.centralwidget)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        spacerItem = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonComputePlot = QtGui.QPushButton(self.centralwidget)
        self.buttonComputePlot.setObjectName(_fromUtf8("buttonComputePlot"))
        self.horizontalLayout.addWidget(self.buttonComputePlot)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "STA/LTA and triggering options", None))
        self.label.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Loaded Trace</span></p></body></html>", None))
        self.label_3.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Trigger Type</span></p></body></html>", None))
        self.comboTrigger.setItemText(0, _translate("STA/LTA and triggering options", "Recursive (STA/LTA)", None))
        self.comboTrigger.setItemText(1, _translate("STA/LTA and triggering options", "Classic (STA/LTA)", None))
        self.comboTrigger.setItemText(2, _translate("STA/LTA and triggering options", "Delayed (STA/LTA)", None))
        self.label_4.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Generic STA/LTA Settings</span></p></body></html>", None))
        self.label_6.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Modify Trigger Parameters </span></p></body></html>", None))
        self.label_2.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Short Time Average Window (s)</span></p></body></html>", None))
        self.label_5.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Long Time Average Window (s)</span></p></body></html>", None))
        self.label_7.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Triggering on </span></p></body></html>", None))
        self.label_8.setText(_translate("STA/LTA and triggering options", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Triggering off</span></p></body></html>", None))
        self.buttonCancel.setText(_translate("STA/LTA and triggering options", "Cancel", None))
        self.buttonComputePlot.setText(_translate("STA/LTA and triggering options", "Compute/Plot", None))

