import logging
import platform

from qtCore import *
from ui.printerWidget import PrinterWidget
from ui.printingWidget import PrintingWidget
from ui.splashWidget import SplashWidget


class MixwareScreen(QWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer

        theme = self._printer.config.get_theme()
        # with open(root_path / "resource" / str(theme) / "style.qss", 'r', encoding='utf-8') as file:
        with open("resource/style.qss", 'r', encoding='utf-8') as file:
            style = file.read()
            qApp.setStyleSheet(style)
            file.close()

        self.stackedLayout = QStackedLayout(self)
        self.splashWidget = SplashWidget(printer)
        self.printerPage = PrinterWidget(printer)
        self.printingPage = PrintingWidget(printer)
        self.printingPage.print_done.connect(self.on_print_done)

        self.init_form()
        self.init_layout()
        self.init_connect()

        if platform.system().lower() == 'windows':
            self.stackedLayout.setCurrentIndex(2)

        # QtCore.QMetaObject.connectSlotsByName(self)
        # self.notify = QLabel(self)
        # self.notify.setFixedSize(380, 80)
        # self.notify.setText("#######################")
        # self.notify.setAlignment(Qt.AlignVCenter)
        # self.notify.setStyleSheet("QLabel {background: rgba(0, 0, 0, 0.75); color: #FFFFFF; border: none; border-radius: 10px; padding-left: 20px;}")
        # self.notify.move(10, 10)

    def init_form(self):
        self.setWindowTitle("Mixware Screen")
        self.resize(self._printer.config.get_window_size())

        self.stackedLayout.setObjectName("stackedLayout")
        self.splashWidget.setObjectName("splashWidget")
        self.printerPage.setObjectName("printerPage")
        self.printingPage.setObjectName("printingPage")

        self.stackedLayout.addWidget(self.splashWidget)
        self.stackedLayout.addWidget(self.printerPage)
        self.stackedLayout.addWidget(self.printingPage)

    def init_layout(self):
        pass

    def init_connect(self):
        self.splashWidget.button.clicked.connect(self.splash_button_clicked)
        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)

    def on_print_done(self):
        self.on_update_printer_status(1)

    def splash_button_clicked(self):
        if self.splashWidget.button.text() == "Start" and self._printer.is_connected():
            self.printerPage.gotoMainPage()
            self.stackedLayout.setCurrentWidget(self.printerPage)
        elif self._printer.is_connecting():
            pass
        else:
            self._printer.connect_serial()

    def set_stacked_index(self, index: int):
        if index != self.stackedLayout.currentIndex():
            self.stackedLayout.setCurrentIndex(index)

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
            elif self.stackedLayout.currentWidget() == self.printingPage:
                self.set_stacked_index(status)
        elif status == 2:
            if self.stackedLayout.currentWidget() == self.printerPage:
                self.printingPage.reset_time()
                self.printingPage.set_file_name(self._printer.printing_information['path'])
                self.set_stacked_index(status)