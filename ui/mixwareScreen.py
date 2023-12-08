import logging
import platform

from qtCore import *
from ui.printerWidget import PrinterWidget
from ui.printingWidget import PrintingWidget
from ui.splashWidget import SplashWidget

class NotifyFrame(QFrame):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_move = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.notify = QLabel(self)
        self.notify.setFixedSize(360, 80)
        self.notify.setText("This is a Mixware Screen message. Click anywhere to close it.")
        self.notify.setWordWrap(True)
        self.notify.setStyleSheet("QLabel {background: rgba(0, 0, 0, 0.75); color: #FFFFFF; border: none; border-radius: 10px; padding-left: 20px;}")
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
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._printer.updatePrinterMessage.connect(self.on_update_printer_message)

        theme = self._printer.config.get_theme()
        # with open(root_path / "resource" / str(theme) / "style.qss", 'r', encoding='utf-8') as file:
        with open("resource/style.qss", 'r', encoding='utf-8') as file:
            style = file.read()
            qApp.setStyleSheet(style)
            file.close()

        self.setWindowTitle("Mixware Screen")
        self.resize(self._printer.config.get_window_size())

        self.stackedLayout = QStackedLayout(self)
        self.stackedLayout.setObjectName("stackedLayout")
        self.splashWidget = SplashWidget(printer)
        self.splashWidget.setObjectName("splashWidget")
        self.splashWidget.button.clicked.connect(self.splash_button_clicked)
        self.stackedLayout.addWidget(self.splashWidget)
        self.printerWidget = PrinterWidget(printer)
        self.printerWidget.setObjectName("printerWidget")
        self.stackedLayout.addWidget(self.printerWidget)
        self.printingWidget = PrintingWidget(printer)
        self.printingWidget.print_done.connect(self.on_print_done)
        self.printingWidget.setObjectName("printingWidget")
        self.stackedLayout.addWidget(self.printingWidget)

        if platform.system().lower() == 'windows':
            self.stackedLayout.setCurrentIndex(2)
        self.notify_frame = NotifyFrame(self)
        self.notify_frame.resize(self.width(), 100)
        self.notify_frame.move(0, 10)
        if platform.system().lower() == 'linux':
            self.notify_frame.hide()
        self.notify_timer = QTimer(self)

    def on_print_done(self):
        self.on_update_printer_status(1)

    def splash_button_clicked(self):
        if self.splashWidget.button.text() == "Start" and self._printer.is_connected():
            self.printerWidget.gotoMainPage()
            self.stackedLayout.setCurrentWidget(self.printerWidget)
        elif self._printer.is_connecting():
            pass
        else:
            self._printer.connect_serial()
        if self.notify_frame.isVisible():
            self.notify_frame.raise_()

    def set_stacked_index(self, index: int):
        if index != self.stackedLayout.currentIndex():
            self.stackedLayout.setCurrentIndex(index)
        if self.notify_frame.isVisible():
            self.notify_frame.raise_()

    @pyqtSlot(int)
    def on_update_printer_status(self, status):
        if status == 0:
            if self.stackedLayout.currentWidget() == self.splashWidget:
                self.splashWidget.button.setText("Update")
                self.splashWidget.tips.setText("No printer detected.")
            else:
                self.set_stacked_index(status)
        elif status == 1:
            if self.stackedLayout.currentWidget() == self.splashWidget:
                self.splashWidget.button.setText("Start")
                self.splashWidget.tips.setText("Click <Start> to start using the printer.")
            elif self.stackedLayout.currentWidget() == self.printingWidget:
                self.set_stacked_index(status)
        elif status == 2:
            if self.stackedLayout.currentWidget() == self.printerWidget:
                self.printingWidget.reset_time()
                self.printingWidget.set_file_name(self._printer.printing_information['path'])
                self.set_stacked_index(status)

    @pyqtSlot(str, int)
    def on_update_printer_message(self, message, level):
        self.notify_frame.set_text(message)
        if self.notify_frame.isHidden():
            self.notify_frame.show()
        self.notify_frame.raise_()

        if level == 1:
            self.notify_timer.singleShot(3000, self.notify_frame.hide)