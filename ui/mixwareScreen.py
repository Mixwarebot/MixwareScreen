import logging
import platform

from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.printerWidget import PrinterWidget
from ui.printingWidget import PrintingWidget
from ui.splashWidget import SplashWidget
from ui.welcomePages.welcomeWidget import WelcomeWidget


class NotifyFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_move = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.notify = QLabel(self)
        self.notify.setFixedSize(360, 80)
        self.notify.setText(self.tr("This is a Mixware Screen message. Click anywhere to close it."))
        self.notify.setWordWrap(True)
        self.notify.setStyleSheet(
            "QLabel {background: rgba(0, 0, 0, 0.75); color: #FFFFFF; border: none; border-radius: 10px; padding-left: 20px;}")
        self.layout.addWidget(self.notify)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.hide()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.is_move = True

    def set_text(self, text):
        self.notify.setText(text)


class MixwareScreen(QWidget):
    updateTranslator = pyqtSignal(str)

    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._printer.updatePrinterMessage.connect(self.on_update_printer_message)

        theme = self._printer.config.get_theme()
        # with open(root_path / "resource" / str(theme) / "style.qss", 'r', encoding='utf-8') as file:
        with open("resource/style.qss", 'r', encoding='utf-8') as file:
            logging.info("Initialize style")
            style = file.read()
            qApp.setStyleSheet(style)
            file.close()

        self.setWindowTitle("Mixware Screen")
        self.resize(self._printer.config.get_window_size())

        self.stackedLayout = QStackedLayout(self)
        self.stackedLayout.setObjectName("stackedLayout")
        self.welcomeWidget = WelcomeWidget(printer)
        self.welcomeWidget.setObjectName("welcomeWidget")
        self.welcomeWidget.updateTranslator.connect(self.on_update_translator)
        self.welcomeWidget.complete.connect(self.on_welcome_complete)
        self.stackedLayout.addWidget(self.welcomeWidget)
        self.splashWidget = SplashWidget(printer)
        self.splashWidget.setObjectName("splashWidget")
        self.splashWidget.button.clicked.connect(self.splash_button_clicked)
        self.stackedLayout.addWidget(self.splashWidget)
        self.printerWidget = PrinterWidget(printer)
        self.printerWidget.setObjectName("printerWidget")
        self.printerWidget.updateTranslator.connect(self.on_update_translator)
        self.stackedLayout.addWidget(self.printerWidget)
        self.printingWidget = PrintingWidget(printer)
        self.printingWidget.print_done.connect(self.on_print_done)
        self.printingWidget.setObjectName("printingWidget")
        self.stackedLayout.addWidget(self.printingWidget)

        self.notify_frame = NotifyFrame(self)
        self.notify_frame.resize(self.width(), 100)
        self.notify_frame.move(0, 10)
        self.notify_frame.hide()
        self.notify_timer = QTimer(self)

        # test
        if platform.system().lower() == 'windows':
            self.stackedLayout.setCurrentIndex(2)
        else:
            if self._printer.config.should_show_welcome:
                self.stackedLayout.setCurrentIndex(0)
            else:
                self.stackedLayout.setCurrentIndex(1)

    def on_print_done(self):
        self.on_update_printer_status(MixwareScreenPrinterStatus.PRINTER_CONNECTED)

    def splash_button_clicked(self):
        if self.splashWidget.button.text() == self.tr("Start") and self._printer.is_connected():
            self.printerWidget.gotoMainPage()
            self.stackedLayout.setCurrentWidget(self.printerWidget)
        elif self._printer.is_connecting():
            pass
        else:
            self._printer.connect_serial()
        if self.notify_frame.isVisible():
            self.notify_frame.raise_()

    def set_stacked_index(self, w: QWidget):
        if w != self.stackedLayout.currentWidget():
            self.stackedLayout.setCurrentWidget(w)
        if self.notify_frame.isVisible():
            self.notify_frame.raise_()

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, status):
        if self.stackedLayout.currentWidget() == self.welcomeWidget:
            return

        if status == MixwareScreenPrinterStatus.PRINTER_DISCONNECTED:
            if self.stackedLayout.currentWidget() == self.splashWidget:
                self.splashWidget.button.setText(self.tr("Update"))
                self.splashWidget.tips.setText(self.tr("No printer detected."))
            else:
                self.set_stacked_index(self.splashWidget)
        elif status == MixwareScreenPrinterStatus.PRINTER_CONNECTED:
            if self.stackedLayout.currentWidget() == self.splashWidget:
                self.splashWidget.button.setText(self.tr("Start"))
                self.splashWidget.tips.setText(self.tr("Click <Start> to start using the printer."))
            elif self.stackedLayout.currentWidget() == self.printingWidget:
                self.set_stacked_index(self.printerWidget)
        elif status == MixwareScreenPrinterStatus.PRINTER_PRINTING:
            if self.stackedLayout.currentWidget() == self.printerWidget:
                self.printingWidget.reset_time()
                self.printingWidget.set_file_name(self._printer.printing_information['path'])
                self.set_stacked_index(self.printingWidget)

    @pyqtSlot(str, int)
    def on_update_printer_message(self, message, level):
        self.notify_frame.set_text(message)
        if self.notify_frame.isHidden():
            self.notify_frame.show()
        self.notify_frame.raise_()

        if level == 1:
            self.notify_timer.singleShot(3000, self.notify_frame.hide)

    @pyqtSlot(str)
    def on_update_translator(self, language: str):
        self.updateTranslator.emit(language)
        self._printer.config.set_language(language)

    def on_welcome_complete(self):
        if self._printer.config.should_show_welcome:
            self._printer.config.set_value('window/welcome', 0)
        if self._printer.is_connected():
            self.set_stacked_index(self.printerWidget)
        else:
            self.set_stacked_index(self.splashWidget)
