import os
import platform

from qtCore import *


class MixwareScreenConfig:
    config = None
    default_file = "/default_config.ini"
    file = "/.config.ini"
    format = QSettings.IniFormat
    width = 400
    height = 1280
    theme = "Light"
    language = "English"
    folder_rootPath = "~/printer_data/gcodes/"

    def __init__(self, path: str):
        self.path = path

        # Create a local config.ini if it does not exist
        if not os.path.isfile(self.file):
            self.reset_local_config()

        # Automatically increment the version number during testing
        self.default_config = QSettings(str(self.path + self.default_file), self.format)
        self.latest_version = self.default_config.value('app/version')
        if platform.system().lower() == 'windows':
            self.latest_version_array = str(self.latest_version).split('.')
            self.default_config.setValue('app/version',
                                         f"{self.latest_version_array[0]}."
                                         f"{self.latest_version_array[1]}."
                                         f"{self.latest_version_array[2]}."
                                         f"{int(self.latest_version_array[3]) + 1}")
            self.default_config.sync()

        self.config = QSettings(str(self.path + self.file), self.format)

        # Check the latest version
        if self.get_version() != self.latest_version:
            self.set_version(self.latest_version)

        self.width = int(self.config.value('window/width'))
        self.height = int(self.config.value('window/height'))
        self.theme = self.config.value('window/theme')
        self.language = self.config.value('window/language')
        self.folder_rootPath = self.config.value('folder/root')

    def set_value(self, key: str, value):
        self.config.setValue(key, value)
        self.config.sync()

    def get_config(self):
        return self.config

    def get_window_size(self):
        return QSize(self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_theme(self, theme: str):
        self.set_value('window/theme', theme)

    def get_theme(self):
        return self.config.value('window/theme')

    def set_language(self, lang: str):
        self.set_value('window/language', lang)

    def get_language(self):
        return self.config.value('window/language')

    def get_folder_rootPath(self):
        return self.folder_rootPath

    def get_version(self):
        return self.config.value('app/version')

    def set_version(self, version: str):
        self.set_value('app/version', version)

    def reset_local_config(self):
        with open(self.path + self.default_file, 'r') as src:
            with open(self.path + self.file, 'w') as dest:
                dest.write(src.read())
