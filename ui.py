# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/tracker_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(447, 101)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.StatusLabel = QtWidgets.QLabel(MainWidget)
        self.StatusLabel.setScaledContents(False)
        self.StatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StatusLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.StatusLabel.setObjectName("StatusLabel")
        self.verticalLayout.addWidget(self.StatusLabel)
        self.frame = QtWidgets.QFrame(MainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.SoundCheckbox = QtWidgets.QCheckBox(self.frame)
        self.SoundCheckbox.setChecked(True)
        self.SoundCheckbox.setObjectName("SoundCheckbox")
        self.horizontalLayout.addWidget(self.SoundCheckbox)
        self.MessegesCheckbox = QtWidgets.QCheckBox(self.frame)
        self.MessegesCheckbox.setChecked(True)
        self.MessegesCheckbox.setObjectName("MessegesCheckbox")
        self.horizontalLayout.addWidget(self.MessegesCheckbox)
        self.TrayCheckbox = QtWidgets.QCheckBox(self.frame)
        self.TrayCheckbox.setChecked(True)
        self.TrayCheckbox.setObjectName("TrayCheckbox")
        self.horizontalLayout.addWidget(self.TrayCheckbox)
        self.ExitButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExitButton.sizePolicy().hasHeightForWidth())
        self.ExitButton.setSizePolicy(sizePolicy)
        self.ExitButton.setObjectName("ExitButton")
        self.horizontalLayout.addWidget(self.ExitButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(MainWidget)
        self.ExitButton.clicked.connect(MainWidget.close)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "Sentient anomaly tracker"))
        self.StatusLabel.setText(_translate("MainWidget", "No anomaly currently present"))
        self.SoundCheckbox.setText(_translate("MainWidget", "Sound"))
        self.MessegesCheckbox.setText(_translate("MainWidget", "Messeges"))
        self.TrayCheckbox.setText(_translate("MainWidget", "Exit to tray"))
        self.ExitButton.setText(_translate("MainWidget", "Exit"))
