import os

from qtCore import *
from ui.base.basePushButton import BasePushButton


class AboutPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.need_reboot_system = False
        self.need_reboot_printer = False
        self._printer = printer
        self._parent = parent

        self._printer.repository.state_changed.connect(self.on_git_state_changed)

        self.setObjectName("aboutPage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 10)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(20, 0, 20, 0)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setAlignment(Qt.AlignCenter)
        self.logo = QLabel()
        self.logo.setFixedSize(320, 128)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setPixmap(QPixmap("resource/icon/Mixware.svg").scaledToHeight(188))
        self.frame_layout.addWidget(self.logo)
        self.name = QLabel()
        self.name.setStyleSheet("font-size:32px; font-weight: bold;")
        self.name.setFixedSize(320, 48)
        self.name.setAlignment(Qt.AlignCenter)
        self.frame_layout.addWidget(self.name)
        self.version_info = QLabel()
        self.version_info.setFixedSize(320, 138)
        self.version_info.setAlignment(Qt.AlignHCenter)
        self.frame_layout.addWidget(self.version_info)
        self.update_button = BasePushButton()
        self.update_button.setStyleSheet("border: 1px solid #D4D4D4;")
        self.update_button.setFixedHeight(64)
        self.update_button.clicked.connect(self.on_update_button_clicked)
        self.frame_layout.addWidget(self.update_button)
        self.update_info = QLabel()
        self.update_info.setObjectName('tips')
        self.update_info.setFixedSize(320, 40)
        self.update_info.setAlignment(Qt.AlignCenter)
        self.frame_layout.addWidget(self.update_info)
        self.layout.addWidget(self.frame)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.name.setText("Mixware Screen")
        self.update_button.setText(self.tr("Check for updates"))
        info = ""
        if self._printer.version():
            info += self.tr("Version: {}\n").format(self._printer.version())

        if "Unknown" not in self._printer.deviceName():
            info += self.tr("Printer Name: {}\n").format(self._printer.deviceName())
            info += self.tr("Printer Version: {}\n").format(self._printer.deviceVersion())
        else:
            info += self.tr("Printer disconnected.\n")

        if self._printer.get_ip_addr("wlan0"):
            info += self.tr("IP Address: {}").format(self._printer.get_ip_addr("wlan0"))
        else:
            info += self.tr("Network not connected.")

        self.version_info.setText(info)

    def on_update_button_clicked(self):
        if self._printer.is_connected():
            self._printer.repository.start_firmware_check()
        else:
            self._printer.repository.start_screen_check()
        self.re_translate_ui()

    def on_update_finished(self):
        print('on_update_finished')
        self._parent.showShadowScreen()
        if self.need_reboot_system:
            ret = self._parent.message.start("Mixware Screen",
                                             self.tr("Mixware Screen update successful,\nrestart to take effect."),
                                             buttons=QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                if self._printer.is_connected() and self.need_reboot_printer:
                    self._printer.printer_reboot()
                os.system('sudo clear')
                os.system('sudo systemctl restart MixwareScreen')

        if self._printer.is_connected():
            if self.need_reboot_printer:
                ret = self._parent.message.start("Mixware Screen", self.tr(
                    "Firmware download is successful,\nrestart the printer to upgrade."),
                                                 buttons=QMessageBox.Yes | QMessageBox.Cancel)
                if ret == QMessageBox.Yes:
                    self._printer.printer_reboot()
            else:
                self._parent.message.start("Mixware Screen", self.tr("Update failed."), buttons=QMessageBox.Yes)
        self._parent.closeShadowScreen()

    def on_git_state_changed(self, state):
        if self._printer.is_connected():
            if state == self.tr("Latest firmware version is Marlin {}.".format(
                    self._printer.repository.get_firmware_latest_version())):
                if self._printer.repository.get_firmware_latest_version() in self._printer.deviceVersion():
                    self._printer.repository.start_screen_check()
                else:
                    _dir = QDir(self._printer.config.get_folder_rootPath())
                    _files = _dir.entryInfoList()
                    for file in _files:
                        if file.isDir() and file.exists(f'{file.absoluteFilePath()}/firmware.cur'):
                            self._printer.repository.set_firmware_path(file.absoluteFilePath())
                            self._printer.repository.start_firmware_download()
                            break
                        if file == _files[-1]:
                            # Motherboard USB disk not found.
                            self._printer.repository.start_screen_check()
            elif state == self.tr("Firmware download successful."):
                self.need_reboot_printer = True
                self._printer.repository.start_screen_check()
            elif state == self.tr("firmware check error.") or state == self.tr("Firmware download error."):
                self._printer.repository.start_screen_check()

        if state == self.tr("Mixware Screen check successful."):
            if self._printer.repository.screen_exist_update():
                self._printer.repository.start_screen_pull()
            else:
                state += self.tr("\nMixware Screen is the latest version.")
                if self.need_reboot_printer:
                    self.on_update_finished()
        elif state == self.tr("Mixware Screen update successful."):
            self.need_reboot_system = True
            self.on_update_finished()
        elif state == self.tr("Mixware Screen check failed.") or state == self.tr("Mixware Screen update failed."):
            if self.need_reboot_printer:
                self.on_update_finished()

        self.update_info.setText(state)

