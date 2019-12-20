#!/bin/env python3
import requests
import json
import sys
from ui import Ui_MainWidget
from time import sleep
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QSystemTrayIcon,
    QMenu, QAction, qApp)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.last_state = None
        self.nodes = {505: "Ruse War Field",
                      510: "Gian Point",
                      550: "Nsu Grid",
                      551: "Ganalen's Grave",
                      552: "Rya",
                      553: "Flexa",
                      554: "H-2 Cloud",
                      555: "R-9 Cloud"}
        self.sounds = {"spawn": QSound("resources/spawn.wav"),
                       "despawn": QSound("resources/despawn.wav")}
        self.icon = QIcon("resources/icon.png")

        # Set up the user interface from Designer.
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        self.setWindowIcon(self.icon)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setToolTip("Sentient tracker")

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.result.connect(self.use_data)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.get_data)
        self.worker_thread.start()

    @pyqtSlot(str)
    def use_data(self, data):
        planet = json.loads(data)

        if planet and not self.last_state:
            code = planet["sfn"]
            text = f"Anomaly present at {self.nodes[code]}"
            self.ui.StatusLabel.setText(text)

            if self.ui.SoundCheckbox.isChecked():
                self.sounds["spawn"].play()

            if self.ui.MessegesCheckbox.isChecked():
                self.tray_icon.showMessage(
                    "Sentient anomaly tracker",
                    text,
                    QSystemTrayIcon.Information,
                    10000)
            self.last_state = True
        elif not planet and self.last_state:
            self.ui.StatusLabel.setText("No anomaly currently present")
            if self.ui.SoundCheckbox.isChecked():
                self.sounds["despawn"].play()

            if self.ui.MessegesCheckbox.isChecked():
                self.tray_icon.showMessage(
                    "Sentient anomaly tracker",
                    "Anomaly despawned",
                    self.icon,
                    2000)
            self.last_state = False

    def closeEvent(self, event):
        if self.ui.TrayCheckbox.isChecked():
            event.ignore()
            self.hide()
            if self.ui.MessegesCheckbox.isChecked():
                self.tray_icon.showMessage(
                    "Sentient anomaly tracker",
                    "Tracker was closed to tray",
                    self.icon,
                    2000)


class Worker(QObject):
    result = pyqtSignal(str)

    @pyqtSlot()
    def get_data(self):
        session = requests.Session()
        url = "http://content.warframe.com/dynamic/worldState.php"
        while True:
            worldstate = session.get(url).json()
            spawn = worldstate["Tmp"]

            self.result.emit(spawn)
            sleep(60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
