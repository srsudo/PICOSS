# -*- coding: utf-8 -*-

"""
Dialog panel to load data from local computer. Functionalities are appended within the main interface.
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
        MainWindow.resize(531, 237)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))

        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)

        self.network_2 = QtGui.QLineEdit(self.centralwidget)
        self.network_2.setObjectName(_fromUtf8("network_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.network_2)

        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)

        self.station_2 = QtGui.QLineEdit(self.centralwidget)
        self.station_2.setObjectName(_fromUtf8("station_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.station_2)

        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_9)

        self.channel_2 = QtGui.QLineEdit(self.centralwidget)
        self.channel_2.setObjectName(_fromUtf8("channel_2"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.channel_2)

        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_10)

        self.location_2 = QtGui.QLineEdit(self.centralwidget)
        self.location_2.setObjectName(_fromUtf8("location_2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.location_2)

        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_12)

        self.label_filename_2 = QtGui.QLabel(self.centralwidget)
        self.label_filename_2.setText(_fromUtf8(""))
        self.label_filename_2.setObjectName(_fromUtf8("label_filename_2"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.label_filename_2)

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.pushButton_3)

        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.pushButton_4)

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label)

        self.day_of_the_year = QtGui.QLineEdit(self.centralwidget)
        self.day_of_the_year.setObjectName(_fromUtf8("day_of_the_year"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.day_of_the_year)
        self.verticalLayout.addLayout(self.formLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Visualize Preprocessed Picking File", None))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Network</span></p></body></html>", None))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Station  </span></p></body></html>", None))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Channel</span></p></body></html>", None))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Location</span></p></body></html>", None))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Filename</span></p></body></html>", None))
        self.pushButton_3.setText(_translate("MainWindow", "Load Picking File", None))
        self.pushButton_4.setText(_translate("MainWindow", "Plot Results", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Day of Year</span></p></body></html>", None))

