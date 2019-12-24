#!/usr/bin/env python3
import requests
import json
import sys
from pathlib import Path
from datetime import datetime
from .ui import Ui_MainWidget
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QSystemTrayIcon, QMessageBox,
    QMenu, QAction, QStyle)
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.last_state = None
        self.last_spawn = None
        self.last_despawn = None
        self.tray_close_shown = False
        self.local_path = Path(__file__).parent
        self.conf_path = self.local_path / "settings.json"
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
        self.ui.SoundCheckbox.stateChanged.connect(self.sound_change)
        self.ui.MessagesCheckbox.stateChanged.connect(self.message_change)
        self.ui.TrayCheckbox.stateChanged.connect(self.tray_change)
        self.ui.PlatfromCombobox.currentTextChanged.connect(self.platform_change)
        info_icon = QIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.ui.HelpButton.setIcon(info_icon)
        self.ui.HelpButton.clicked.connect(self.show_help)

        self.handle_files()
        self.setWindowIcon(self.icon)

        self.TrayIcon = QSystemTrayIcon(self)
        self.TrayIcon.setIcon(self.icon)
        self.TrayIcon.setToolTip("No anomaly")
        self.TrayIcon.activated.connect(self.double_click)

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_save)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.TrayIcon.setContextMenu(tray_menu)

        self.worker_thread = QThread(parent=self)
        self.worker = Worker()
        self.worker.result.connect(self.use_data)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.start_worker)
        self.worker_thread.start()
        self.ui.CheckButton.clicked.connect(self.worker.get_data)

        self.load_config()

    def load_config(self):
        if self.conf_path.is_file():
            with open(self.conf_path) as f:
                self.settings = json.load(f)
        else:
            self.settings = {"sounds": True,
                             "messages": True,
                             "tray": True,
                             "platform": "PC"}

        if not self.settings["sounds"]:
            self.ui.SoundCheckbox.setChecked(False)
        if not self.settings["messages"]:
            self.ui.MessagesCheckbox.setChecked(False)
        if not self.settings["tray"]:
            self.ui.TrayCheckbox.setChecked(False)
        else:
            self.TrayIcon.show()

        platform = self.settings["platform"]
        if platform == "PC":
            self.worker.get_data()
        else:
            self.ui.PlatfromCombobox.setCurrentText(platform)

    def save_config(self):
        with open(self.conf_path, "w") as f:
            json.dump(self.settings, f, indent=4)

    def handle_files(self):
        if hasattr(sys, "_MEIPASS"):
            meipass_path = Path(sys._MEIPASS) / 'resources'
        else:
            meipass_path = None
        resource_path = self.local_path / "resources"

        spawn_path = resource_path / "spawn.wav"
        if spawn_path.is_file():
            spawn_sound = f"{spawn_path}"
        elif meipass_path:
            spawn_sound = f"{meipass_path / 'spawn.wav'}"

        despawn_path = resource_path / "despawn.wav"
        if despawn_path.is_file():
            despawn_sound = f"{despawn_path}"
        elif meipass_path:
            despawn_sound = f"{meipass_path / 'despawn.wav'}"

        if meipass_path:
            icon_file = f"{meipass_path / 'icon.png'}"
        else:
            icon_file = f"{resource_path / 'icon.png'}"

        self.sounds = {"spawn": QSound(spawn_sound),
                       "despawn": QSound(despawn_sound)}
        self.icon = QIcon(icon_file)

    @pyqtSlot(int)
    def sound_change(self, num):
        if num == 0:
            state = False
        elif num == 2:
            state = True

        self.settings["sounds"] = state

    @pyqtSlot(int)
    def message_change(self, num):
        if num == 0:
            state = False
        elif num == 2:
            state = True

        self.settings["messages"] = state

    @pyqtSlot(int)
    def tray_change(self, num):
        if num == 0:
            self.TrayIcon.hide()
            state = False
        elif num == 2:
            self.TrayIcon.show()
            state = True

        self.settings["tray"] = state

    @pyqtSlot(str)
    def platform_change(self, platform):
        self.settings["platform"] = platform
        self.worker.current_platform = platform
        self.worker.get_data()

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
            self.TrayIcon.setToolTip("Connection error")
            self.last_state = None
            return
        planet = json.loads(data)

        if planet and not self.last_state:
            code = planet["sfn"]
            text = f"Anomaly present at {self.nodes[code]}"
            self.ui.StatusLabel.setText(text)

            if self.ui.SoundCheckbox.isChecked():
                self.sounds["spawn"].play()

            if self.ui.MessagesCheckbox.isChecked():
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    text,
                    self.icon,
                    10000)

            if self.last_state is False:
                self.last_spawn = datetime.now().strftime("%H:%M:%S")
                self.ui.SpawnLabel.setText(self.last_spawn)
                tool_tip = f"Anomaly at {self.nodes[code]} since {self.last_spawn}"
            else:
                tool_tip = f"Anomaly at {self.nodes[code]}"
            self.TrayIcon.setToolTip(tool_tip)
            self.last_state = True

        elif not planet and self.last_state:
            self.ui.StatusLabel.setText("No anomaly currently present")
            self.last_despawn = datetime.now().strftime("%H:%M:%S")
            self.ui.DespawnLabel.setText(self.last_despawn)
            if self.ui.SoundCheckbox.isChecked():
                self.sounds["despawn"].play()

            if self.ui.MessagesCheckbox.isChecked():
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    "Anomaly despawned",
                    self.icon,
                    2000)
            self.TrayIcon.setToolTip(f"No anomaly since {self.last_despawn}")
            self.last_state = False
        elif not planet and self.last_state is None:
            self.ui.StatusLabel.setText("No anomaly currently present")
            self.TrayIcon.setToolTip("No anomaly")
            self.last_state = False

    @pyqtSlot()
    def quit_save(self):
        self.save_config()
        QApplication.quit()

    @pyqtSlot()
    def show_help(self):
        text = ("This application will notify you when a sentient anomaly spawns.<br>"
                "The spawns last for around 30min and take around 3h (+- 30min) to spawn.<br>"
                "More information, the source code and new versions can be found on the "
                "<a href='https://github.com/Kanjirito/wf-sentient-tracker'>GitHub page.</a>")

        QMessageBox.about(self,
                          "Help window",
                          text)

    def closeEvent(self, event):
        if self.ui.TrayCheckbox.isChecked():
            event.ignore()
            self.hide()
            if self.ui.MessagesCheckbox.isChecked() and not self.tray_close_shown:
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    "Tracker was closed to tray",
                    self.icon,
                    2000)
                self.tray_close_shown = True
        else:
            self.save_config()

    def double_click(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()


class Worker(QObject):
    result = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_url = "http://content{}.warframe.com/dynamic/worldState.php"
        self.current_platform = "PC"
        self.platforms = {"PC": "",
                          "PS4": ".ps4",
                          "XB1": ".xb1"}

    @pyqtSlot()
    def start_worker(self):
        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.get_data)

    @pyqtSlot()
    def get_data(self):
        url = self.base_url.format(self.platforms[self.current_platform])
        try:
            r = self.session.get(url, timeout=5)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            self.result.emit("Error")
        else:
            worldstate = r.json()
            spawn = worldstate["Tmp"]
            self.result.emit(spawn)


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
