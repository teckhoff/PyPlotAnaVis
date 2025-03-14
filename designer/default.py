# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\designer\default.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 300)
        MainWindow.setMinimumSize(QtCore.QSize(700, 300))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.AmplitudeBox = QtWidgets.QHBoxLayout()
        self.AmplitudeBox.setObjectName("AmplitudeBox")
        self.AmplitudeLabel = QtWidgets.QLabel(self.centralwidget)
        self.AmplitudeLabel.setScaledContents(False)
        self.AmplitudeLabel.setObjectName("AmplitudeLabel")
        self.AmplitudeBox.addWidget(self.AmplitudeLabel)
        spacerItem = QtWidgets.QSpacerItem(23, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.AmplitudeBox.addItem(spacerItem)
        self.AmplitudeTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.AmplitudeTextBox.setText("")
        self.AmplitudeTextBox.setObjectName("AmplitudeTextBox")
        self.AmplitudeBox.addWidget(self.AmplitudeTextBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.AmplitudeBox.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.AmplitudeBox)

        self.FrequencyBox = QtWidgets.QHBoxLayout()
        self.FrequencyBox.setObjectName("FrequencyBox")
        self.FrequencyLabel = QtWidgets.QLabel(self.centralwidget)
        self.FrequencyLabel.setObjectName("FrequencyLabel")
        self.FrequencyBox.addWidget(self.FrequencyLabel)
        spacerItem2 = QtWidgets.QSpacerItem(19, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.FrequencyBox.addItem(spacerItem2)
        self.FrequencyTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.FrequencyTextBox.setObjectName("FrequencyTextBox")
        self.FrequencyBox.addWidget(self.FrequencyTextBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.FrequencyBox.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.FrequencyBox)

        self.OffsetBox = QtWidgets.QHBoxLayout()
        self.OffsetBox.setObjectName("OffsetBox")
        self.OffsetLabel = QtWidgets.QLabel(self.centralwidget)
        self.OffsetLabel.setObjectName("OffsetLabel")
        self.OffsetBox.addWidget(self.OffsetLabel)
        spacerItem4 = QtWidgets.QSpacerItem(39, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.OffsetBox.addItem(spacerItem4)
        self.OffsetTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.OffsetTextBox.setObjectName("OffsetTextBox")
        self.OffsetBox.addWidget(self.OffsetTextBox)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.OffsetBox.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.OffsetBox)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_npy_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_npy_file.setObjectName("actionOpen_npy_file")
        self.menuFile.addAction(self.actionOpen_npy_file)
        self.menubar.addAction(self.menuFile.menuAction())
        self.AmplitudeLabel.setBuddy(self.AmplitudeTextBox)
        self.FrequencyLabel.setBuddy(self.FrequencyTextBox)
        self.OffsetLabel.setBuddy(self.OffsetTextBox)

        self.retranslateUi(MainWindow)
        self.AmplitudeTextBox.inputRejected.connect(self.AmplitudeTextBox.clear)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.AmplitudeTextBox, self.FrequencyTextBox)
        MainWindow.setTabOrder(self.FrequencyTextBox, self.OffsetTextBox)
        MainWindow.setTabOrder(self.OffsetTextBox, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.textEdit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AmplitudeLabel.setText(_translate("MainWindow", "Amplitude:"))
        self.FrequencyLabel.setText(_translate("MainWindow", "Frequency:"))
        self.OffsetLabel.setText(_translate("MainWindow", "Offset:"))
        self.pushButton.setText(_translate("MainWindow", "Start Plotting"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_npy_file.setText(_translate("MainWindow", "Open .npy file"))
