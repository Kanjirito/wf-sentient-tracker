#!/usr/bin/env python3
import requests
import json
import sys
from pathlib import Path
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
        self.tray_close_shown = False
        self.nodes = {505: "Ruse War Field",
                      510: "Gian Point",
                      550: "Nsu Grid",
                      551: "Ganalen's Grave",
                      552: "Rya",
                      553: "Flexa",
                      554: "H-2 Cloud",
                      555: "R-9 Cloud"}

        # Set up the user interface from Designer.
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        self.ui.SpawnButton.clicked.connect(self.play_spawn)
        self.ui.DespawnButton.clicked.connect(self.play_despawn)

        self.handle_files()
        self.setWindowIcon(self.icon)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setToolTip("No anomaly")
        self.tray_icon.activated.connect(self.double_click)

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

    def handle_files(self):
        if hasattr(sys, "_MEIPASS"):
            meipass_path = Path(sys._MEIPASS) / 'resources'
        else:
            meipass_path = None
        local_path = Path(".") / "resources"

        spawn_path = local_path / "spawn.wav"
        if spawn_path.is_file():
            spawn_sound = f"{spawn_path}"
        elif meipass_path:
            spawn_sound = f"{meipass_path / 'spawn.wav'}"

        despawn_path = local_path / "despawn.wav"
        if despawn_path.is_file():
            despawn_sound = f"{despawn_path}"
        elif meipass_path:
            despawn_sound = f"{meipass_path / 'despawn.wav'}"

        if meipass_path:
            icon_file = f"{meipass_path / 'icon.png'}"
        else:
            icon_file = f"{local_path / 'icon.png'}"

        self.sounds = {"spawn": QSound(spawn_sound),
                       "despawn": QSound(despawn_sound)}
        self.icon = QIcon(icon_file)

    @pyqtSlot()
    def play_spawn(self):
        self.sounds["spawn"].play()

    @pyqtSlot()
    def play_despawn(self):
        self.sounds["despawn"].play()

    @pyqtSlot(str)
    def use_data(self, data):
        if data == "Error":
            self.ui.StatusLabel.setText("Connection error")
            self.tray_icon.setToolTip("Connection error")
            self.last_state = None
            return
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
                    self.icon,
                    10000)
            self.tray_icon.setToolTip(f"Anomaly at {self.nodes[code]}")
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
            self.tray_icon.setToolTip("No anomaly")
            self.last_state = False
        elif not planet and self.last_state is None:
            self.ui.StatusLabel.setText("No anomaly currently present")
            self.tray_icon.setToolTip("No anomaly")
            self.last_state = False

    def closeEvent(self, event):
        if self.ui.TrayCheckbox.isChecked():
            event.ignore()
            self.hide()
            if self.ui.MessegesCheckbox.isChecked() and not self.tray_close_shown:
                self.tray_icon.showMessage(
                    "Sentient anomaly tracker",
                    "Tracker was closed to tray",
                    self.icon,
                    2000)
                self.tray_close_shown = True

    def double_click(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()


class Worker(QObject):
    result = pyqtSignal(str)

    @pyqtSlot()
    def get_data(self):
        session = requests.Session()
        url = "http://content.warframe.com/dynamic/worldState.php"
        while True:
            try:
                r = session.get(url, timeout=5)
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(e)
                self.result.emit("Error")
            else:
                worldstate = r.json()
                spawn = worldstate["Tmp"]
                self.result.emit(spawn)
            sleep(60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
