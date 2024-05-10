from qtCore import *
from ui.pages.welcomePages.welcomeMainPage import WelcomeMainPage
from ui.pages.welcomePages.welcomeStartPage import WelcomeStartPage


class WelcomeWidget(QWidget):
    updateTranslator = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self.setObjectName("welcomeWidget")
        self.layout = QStackedLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.main_page = WelcomeMainPage(printer)
        self.main_page.complete.connect(self.goto_start_page)
        self.main_page.updateTranslator.connect(self.on_update_translator)
        self.layout.addWidget(self.main_page)
        self.start_page = WelcomeStartPage()
        self.start_page.start_button.clicked.connect(self.on_start_button_clicked)
        self.layout.addWidget(self.start_page)

    def showEvent(self, a0: QShowEvent) -> None:
        self.layout.setCurrentIndex(0)

    @pyqtSlot()
    def goto_start_page(self):
        self.layout.setCurrentWidget(self.start_page)

    @pyqtSlot()
    def on_start_button_clicked(self):
        self.complete.emit()

    @pyqtSlot(str)
    def on_update_translator(self, language: str):
        self.updateTranslator.emit(language)
