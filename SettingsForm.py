# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(234, 409)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 370, 161, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox1 = QtWidgets.QGroupBox(Dialog)
        self.groupBox1.setGeometry(QtCore.QRect(10, 10, 211, 351))
        self.groupBox1.setObjectName("groupBox1")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 191, 20))
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.groupBox1)
        self.label.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox1)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 71, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 100, 91, 20))
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox1)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 71, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 160, 191, 20))
        self.lineEdit_3.setInputMask("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox1)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 71, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 210, 191, 20))
        self.lineEdit_4.setInputMask("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton = QtWidgets.QPushButton(self.groupBox1)
        self.pushButton.setGeometry(QtCore.QRect(10, 250, 191, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox1)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 280, 191, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox1)
        self.checkBox.setGeometry(QtCore.QRect(10, 320, 81, 17))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.groupBox1.setTitle(_translate("Dialog", "Database Settings"))
        self.label.setText(_translate("Dialog", "Server name"))
        self.label_2.setText(_translate("Dialog", "Port"))
        self.label_3.setText(_translate("Dialog", "User name"))
        self.label_4.setText(_translate("Dialog", "Password"))
        self.pushButton.setText(_translate("Dialog", "Load settings"))
        self.pushButton_2.setText(_translate("Dialog", "Save settings (encrypted)"))
        self.checkBox.setText(_translate("Dialog", "Load default"))
