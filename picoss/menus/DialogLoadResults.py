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

        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_10)

        self.label_filename_1 = QtGui.QLabel(self.centralwidget)
        self.label_filename_1.setText(_fromUtf8(""))
        self.label_filename_1.setObjectName(_fromUtf8("label_filename_1"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_filename_1)

        ###############################################################################
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_12)

        self.label_filename_2 = QtGui.QLabel(self.centralwidget)
        self.label_filename_2.setText(_fromUtf8(""))
        self.label_filename_2.setObjectName(_fromUtf8("label_filename_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_filename_2)
        #####################################################################################3


        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.pushButton_3)

        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.pushButton_4)


        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.pushButton_5)


        self.verticalLayout.addLayout(self.formLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Visualize Results", "Visualize Results", None))
        self.label_10.setText(_translate("Visualize Results", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Filename Trace</span></p></body></html>", None))
        self.label_12.setText(_translate("Visualize Results", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Filename Results</span></p></body></html>", None))
        self.pushButton_3.setText(_translate("Visualize Results", "Load Results File", None))
        self.pushButton_4.setText(_translate("Visualize Results", "Plot Results", None))
        self.pushButton_5.setText(_translate("VVisualize Results", "Load Main Trace", None))