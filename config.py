from qtCore import *


class MixwareScreenConfig:
    config = None
    file = "/config.ini"
    format = QSettings.IniFormat
    width = 400
    height = 1280
    theme = "Light"
    language = "English"
    folder_rootPath = "~/printer_data/gcodes/"

    def __init__(self, path: str):
        self.config = QSettings(str(path + self.file), self.format)

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

    def set_version(self, version:str):
        self.set_value('app/version', version)
