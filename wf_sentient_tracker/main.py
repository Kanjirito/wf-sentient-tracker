#!/usr/bin/env python3
import requests
import json
import sys
import os
import subprocess
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
    get_data_signal = pyqtSignal()
    change_platform_signal = pyqtSignal(str)
    quit_signal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.tray_close_shown = False
        self.current_platform = "PC"
        self.nodes = {505: "Ruse War Field",
                      510: "Gian Point",
                      550: "Nsu Grid",
                      551: "Ganalen's Grave",
                      552: "Rya",
                      553: "Flexa",
                      554: "H-2 Cloud",
                      555: "R-9 Cloud"}
        self.last_state = {"PC": None,
                           "PS4": None,
                           "XB1": None}
        self.time_stamps = {"PC": {"spawn": None,
                                   "despawn": None},
                            "PS4": {"spawn": None,
                                    "despawn": None},
                            "XB1": {"spawn": None,
                                    "despawn": None}}

        # Set up the user interface from Designer.
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        self.ui.SpawnButton.clicked.connect(self.play_spawn)
        self.ui.DespawnButton.clicked.connect(self.play_despawn)
        self.ui.TrayCheckbox.stateChanged.connect(self.tray_change)
        self.ui.PlatformCombobox.currentTextChanged.connect(self.platform_change)
        info_icon = QIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.ui.HelpButton.setIcon(info_icon)
        self.ui.HelpButton.clicked.connect(self.show_help)
        self.ui.DirectoryButton.clicked.connect(self.open_directory)

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

        # Worker set up and signal connection
        self.worker_thread = QThread(parent=self)
        self.worker = Worker()
        self.worker.result.connect(self.use_data)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.start_worker)
        self.get_data_signal.connect(self.worker.get_data)
        self.change_platform_signal.connect(self.worker.set_platform)
        self.ui.CheckButton.clicked.connect(self.worker.get_data)
        self.quit_signal.connect(self.worker.stop_worker)
        self.worker_thread.start()

        self.load_config()

    def load_config(self):
        '''
        Loads the configuration file and changes states if not default
        '''
        if self.conf_path.is_file():
            with open(self.conf_path) as f:
                settings = json.load(f)
        else:
            settings = {}

        if not settings.get("sounds", True):
            self.ui.SoundCheckbox.setChecked(False)
        if not settings.get("messages", True):
            self.ui.MessagesCheckbox.setChecked(False)
        if not settings.get("hide", True):
            self.ui.TrayhideCheckbox.setChecked(False)
        if settings.get("hide_shown", False):
            self.tray_close_shown = True
        if not settings.get("tray", True):
            self.ui.TrayCheckbox.setChecked(False)
        else:
            self.TrayIcon.show()

        platform = settings.get("platform", "PC")
        if platform == "PC":
            self.get_data_signal.emit()
        else:
            self.ui.PlatformCombobox.setCurrentText(platform)

    def handle_files(self):
        '''
        Deals with the paths for the files
        '''
        # _MEIPASS is the temp directory used by the .exe
        if hasattr(sys, "_MEIPASS"):
            defualt_path = Path(sys._MEIPASS) / "resources"
        else:
            defualt_path = Path(__file__).resolve().parent / "resources"

        # Determines the base path for the config/custom files
        dot_conf_path = Path.home() / ".config"
        if dot_conf_path.is_dir():
            self.base_path = dot_conf_path / "sentient-tracker"
        else:
            self.base_path = Path.home() / ".sentient-tracker"

        self.base_path.mkdir(parents=True, exist_ok=True)
        self.conf_path = self.base_path / "settings.json"

        spawn_path = self.base_path / "spawn.wav"
        if spawn_path.is_file():
            spawn_sound = f"{spawn_path}"
        else:
            spawn_sound = f"{defualt_path / 'spawn.wav'}"

        despawn_path = self.base_path / "despawn.wav"
        if despawn_path.is_file():
            despawn_sound = f"{despawn_path}"
        else:
            despawn_sound = f"{defualt_path / 'despawn.wav'}"

        icon_file = f"{defualt_path / 'icon.png'}"
        self.sounds = {"spawn": QSound(spawn_sound),
                       "despawn": QSound(despawn_sound)}
        self.icon = QIcon(icon_file)

    @pyqtSlot()
    def open_directory(self):
        '''
        Opens to configuration directory using the default file browser
        '''
        if sys.platform == "win32":
            os.startfile(self.base_path)
        else:
            if sys.platform == "darwin":
                opener = "open"
            else:
                opener = "xdg-open"
            subprocess.call([opener, self.base_path])

    @pyqtSlot(int)
    def tray_change(self, num):
        if num == 0:
            self.TrayIcon.hide()
        elif num == 2:
            self.TrayIcon.show()

    @pyqtSlot(str)
    def platform_change(self, platform):
        self.last_state[self.current_platform] = None
        self.change_platform_signal.emit(platform)
        self.get_data_signal.emit()
        self.current_platform = platform

    @pyqtSlot()
    def play_spawn(self):
        self.sounds["spawn"].play()

    @pyqtSlot()
    def play_despawn(self):
        self.sounds["despawn"].play()

    @pyqtSlot(str)
    def use_data(self, data):
        '''
        Deals with the data from the world state
        '''
        platform = self.ui.PlatformCombobox.currentText()
        state = self.last_state[platform]
        if data == "Error":
            self.ui.StatusLabel.setText("Connection error")
            self.TrayIcon.setToolTip("Connection error")
            self.last_state[platform] = None
            return
        planet = json.loads(data)

        if planet and not state:
            code = planet["sfn"]

            if self.ui.SoundCheckbox.isChecked():
                self.sounds["spawn"].play()

            if self.ui.MessagesCheckbox.isChecked():
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    f"Anomaly present at {self.nodes[code]}",
                    self.icon,
                    10000)

            if state is False:
                time = datetime.now().strftime("%H:%M:%S")
                self.time_stamps[platform]["spawn"] = time
            self.last_state[platform] = True
            self.update_text(platform, planet)

        elif not planet and state:
            time = datetime.now().strftime("%H:%M:%S")
            self.time_stamps[platform]["despawn"] = time

            if self.ui.SoundCheckbox.isChecked():
                self.sounds["despawn"].play()

            if self.ui.MessagesCheckbox.isChecked():
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    "Anomaly despawned",
                    self.icon,
                    2000)
            self.last_state[platform] = False
            self.update_text(platform, planet)

        elif not planet and state is None:
            if self.ui.MessagesCheckbox.isChecked():
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    "No anomaly",
                    self.icon,
                    2000)
            self.last_state[platform] = False

    def update_text(self, platform, planet):
        '''
        Updates the labels and tool tips
        '''
        spawn_stamp = self.time_stamps[platform]["spawn"]
        despawn_stamp = self.time_stamps[platform]["despawn"]
        state = self.last_state[platform]

        if state:
            code = planet["sfn"]
            status_str = f"Anomaly at {self.nodes[code]}"
            if spawn_stamp is None:
                tool_tip = f"Anomaly at {self.nodes[code]}"
            else:
                tool_tip = f"Anomaly at {self.nodes[code]} since {spawn_stamp}"
        else:
            status_str = "No anomaly currently present"
            if despawn_stamp is None:
                tool_tip = "No anomaly"
            else:
                tool_tip = f"No anomaly since {despawn_stamp}"

        if spawn_stamp:
            spawn_str = spawn_stamp
        else:
            spawn_str = "Unknown"

        if despawn_stamp:
            despawn_str = despawn_stamp
        else:
            despawn_str = "Unknown"

        self.ui.SpawnLabel.setText(spawn_str)
        self.ui.DespawnLabel.setText(despawn_str)
        self.TrayIcon.setToolTip(tool_tip)
        self.ui.StatusLabel.setText(status_str)

    @pyqtSlot()
    def quit_save(self):
        '''
        Gets the current settings from the UI and saves them to the config
        file then stops the QThread with the worker and closes the app
        '''
        self.quit_signal.emit()

        if self.ui.SoundCheckbox.checkState() == 2:
            sounds = True
        else:
            sounds = False

        if self.ui.MessagesCheckbox.checkState() == 2:
            messages = True
        else:
            messages = False

        if self.ui.TrayCheckbox.checkState() == 2:
            tray = True
        else:
            tray = False

        if self.ui.TrayhideCheckbox.checkState() == 2:
            hide = True
        else:
            hide = False

        platform = self.ui.PlatformCombobox.currentText()
        settings = {"sounds": sounds,
                    "messages": messages,
                    "tray": tray,
                    "hide": hide,
                    "hide_shown": self.tray_close_shown,
                    "platform": platform}

        self.base_path.mkdir(parents=True, exist_ok=True)
        with open(self.conf_path, "w") as f:
            json.dump(settings, f, indent=4)

        QApplication.quit()

    @pyqtSlot()
    def show_help(self):
        '''
        Shows a help/about window
        '''
        text = ("This application will notify you when a sentient anomaly spawns.<br>"
                "The spawns last for around 30min and take around 3h (+- 30min) to spawn.<br>"
                "More information, the source code and new versions can be found on the "
                "<a href='https://github.com/Kanjirito/wf-sentient-tracker'>GitHub page.</a>")

        QMessageBox.about(self,
                          "Help window",
                          text)

    def closeEvent(self, event):
        '''
        Overrides the quit event to allow tray hiding.
        '''
        event.ignore()
        if self.ui.TrayhideCheckbox.isEnabled() and self.ui.TrayhideCheckbox.isChecked():
            self.hide()
            if self.ui.MessagesCheckbox.isChecked() and not self.tray_close_shown:
                self.TrayIcon.showMessage(
                    "Sentient anomaly tracker",
                    "Tracker was closed to tray",
                    self.icon,
                    2000)
                self.tray_close_shown = True
        else:
            self.quit_save()

    def double_click(self, reason):
        '''
        Double click tray icon to show the window
        '''
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()


class Worker(QObject):
    '''
    Worker that lives in a QThread and checks the API every 60s
    '''
    result = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_url = "http://content{}.warframe.com/dynamic/worldState.php"
        self.current_platform = "PC"
        self.platforms = {"PC": "",
                          "PS4": ".ps4",
                          "XB1": ".xb1"}

    @pyqtSlot(str)
    def set_platform(self, platform):
        '''
        Changes the currently selected platform. Uses slots to avoid any
        problems with threads.
        '''
        self.current_platform = platform

    @pyqtSlot()
    def start_worker(self):
        '''
        Creates and starts the worker
        '''
        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.get_data)
        self.timer.start()

    @pyqtSlot()
    def stop_worker(self):
        self.timer.stop()
        self.thread().quit()

    @pyqtSlot()
    def get_data(self):
        '''
        Gets the data and emits a signal
        '''
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
