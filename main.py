# This Python file uses the following encoding: utf-8
import logging
import os
import platform
import sys
from pathlib import Path

from config import MixwareScreenConfig
from gitRepository import GitRepository
from logger import MixLogger
from printer import MixwareScreenPrinter
from qtCore import *
from server import Server
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
    try:
        QCoreApplication.setOrganizationName('rootFolder')
        app = QApplication([])

        root_path = Path(__file__).resolve().parent

        config = MixwareScreenConfig(str(root_path))

        # Only used during development phase
        if not is_release:
            # Output translation file
            trans()

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

        if is_release:
            app.setOverrideCursor(QCursor(QtCore.Qt.BlankCursor))

        mixwareScreen = MixwareScreen(printer)
        if is_release:
            mixwareScreen.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
            mixwareScreen.showFullScreen()
        else:
            mixwareScreen.show()
        mixwareScreen.updateTranslator.connect(reInstallTranslator)

        httpServer = Server(printer)
        thread = QThread()
        httpServer.moveToThread(thread)
        thread.started.connect(httpServer.start_server)
        thread.start()

        sys.exit(app.exec())
    except:
        os.system('sudo clear')
        os.system("./scripts/mixwareScreen-install.sh")
