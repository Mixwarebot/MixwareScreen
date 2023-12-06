# This Python file uses the following encoding: utf-8
import logging
import os
import platform
import sys
from pathlib import Path

from config import MixwareScreenConfig
from gitRepository import GitRepository
from qtCore import *

from logger import MixLogger
from printer import MixwareScreenPrinter
from ui.mixwareScreen import MixwareScreen

def trans():
    cmd = "pylupdate5 "
    for root, ds, fs in os.walk('.'):
        for f in fs:
            if f.endswith('.py'):
                name = os.path.join(root, f)
                cmd += name
                cmd += ' '
    os.system(cmd + '-ts ./resource/i18n/en/en.ts -noobsolete')
    os.system(cmd + '-ts ./resource/i18n/zh_CN/zh_CN.ts -noobsolete')

def reInstallTranslator(language="English"):
    app.removeTranslator(translator)

    if language == "Chinese":
        translator.load('zh_CN.qm', 'resource/i18n/zh_CN')
    else:
        translator.load('en.qm', 'resource/i18n/en')

    app.installTranslator(translator)

if __name__ == "__main__":
    QCoreApplication.setOrganizationName('rootFolder')
    app = QApplication([])

    root_path = Path(__file__).resolve().parent

    config = MixwareScreenConfig(str(root_path))

    # 只用于开发阶段
    if platform.system().lower() == 'windows':
        # 输出翻译文件
        trans()
        # 子版本号叠加
        version = config.get_version().split('.')
        config.set_version(f"{version[0]}.{version[1]}.{version[2]}.{int(version[3])+1}")

    if platform.system().lower() == 'linux':
        os.system('pip3 install Image')

    ms_logger = MixLogger()
    ms_logger.log_file = root_path / "MixwareScreen.log"
    ms_logger.software_version = config.get_version() + ".alpha"
    ms_logger.setup_logging()

    logging.info("Initializing Mixware Screen")
    printer = MixwareScreenPrinter()
    printer.config = config
    printer.repository = GitRepository(str(root_path))
    printer._version = ms_logger.software_version

    # init translator
    translator = QTranslator()
    reInstallTranslator(config.get_language())

    if platform.system().lower() == 'linux':
        app.setOverrideCursor(QCursor(QtCore.Qt.BlankCursor))
    mixwareScreen = MixwareScreen(printer)
    if platform.system().lower() == 'windows':
        mixwareScreen.show()
    elif platform.system().lower() == 'linux':
        mixwareScreen.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        mixwareScreen.showFullScreen()
    mixwareScreen.printerWidget.updateTranslator.connect(reInstallTranslator)

    sys.exit(app.exec())
