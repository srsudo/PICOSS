# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nuevo_dialog_save.ui'
#
# Created: Sat Jul 20 19:01:55 2019
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
        MainWindow.resize(491, 220)
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
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_4)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.pushButton)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.filename = QtGui.QLineEdit(self.centralwidget)
        self.filename.setObjectName(_fromUtf8("filename"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.filename)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonCancel = QtGui.QPushButton(self.centralwidget)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        spacerItem = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonSave = QtGui.QPushButton(self.centralwidget)
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))
        self.horizontalLayout.addWidget(self.buttonSave)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Save Segmentation Table", "Save Segmentation Table", None))
        self.label.setText(_translate("Save Segmentation Table", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Destination Folder</span></p></body></html>", None))
        self.pushButton.setText(_translate("Save Segmentation Table", "Browse Folder", None))
        self.label_2.setText(_translate("Save Segmentation Table", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Filename </span></p></body></html>", None))
        self.label_3.setText(_translate("Save Segmentation Table", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Saving Format</span></p><p align=\"center\"><br/></p></body></html>", None))
        self.comboBox.setItemText(0, _translate("Save Segmentation Table", ".npy", None))
        self.comboBox.setItemText(1, _translate("Save Segmentation Table", ".mat", None))
        self.comboBox.setItemText(2, _translate("Save Segmentation Table", ".p", None))
        self.buttonCancel.setText(_translate("Save Segmentation Table", "Cancel", None))
        self.buttonSave.setText(_translate("Save Segmentation Table", "Save", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

