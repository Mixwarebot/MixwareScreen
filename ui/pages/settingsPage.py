# from main import installTranslator

from qtCore import *
# from ui.pages.helpPage import HelpPage
from ui.pages.languagePage import LanguagePage
from ui.pages.machinePages.machinePage import MachinePage
from ui.pages.nozzlePage import NozzlePage
from ui.pages.aboutPage import AboutPage
from ui.pages.resetPage import ResetPage
from ui.components.settingsButton import SettingsButton
from ui.pages.wlanPage import WlanPage


class SettingsPage(QWidget):
    new_trans = pyqtSignal(str)

    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("settingsPage")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.machinePage = MachinePage(self._printer, self._parent)
        self.machine = SettingsButton()
        self.machine.clicked.connect(self.gotoMachinePage)
        self.layout.addWidget(self.machine)

        self.nozzlePage = NozzlePage(self._printer, self._parent)
        self.nozzle = SettingsButton()
        self.nozzle.clicked.connect(self.gotoNozzlePage)
        self.layout.addWidget(self.nozzle)

        self.wlanPage = WlanPage(self._printer, self._parent)
        QScroller.grabGesture(self.wlanPage, QScroller.TouchGesture)
        self.wlan = SettingsButton()
        self.wlan.clicked.connect(self.gotoWLANPage)
        self.layout.addWidget(self.wlan)

        self.theme = SettingsButton()
        # self.layout.addWidget(self.theme)

        self.languagePage = LanguagePage(self._printer, self._parent)
        self.language = SettingsButton()
        self.language.clicked.connect(self.gotoLanguagePage)
        self.layout.addWidget(self.language)

        self.user_manual = SettingsButton()
        # self.user_manual.clicked.connect(self.gotoWLANPage)
        # self.layout.addWidget(self.user_manual)

        self.resetPage = ResetPage(self._printer, self._parent)
        self.restore_factory = SettingsButton()
        self.restore_factory.clicked.connect(self.on_restore_factory_clicked)
        self.layout.addWidget(self.restore_factory)

        self.aboutPage = AboutPage(self._printer, self._parent)
        self.about = SettingsButton()
        self.about.clicked.connect(self.gotoAboutPage)
        self.layout.addWidget(self.about)

        # self.helpPage = HelpPage(self._printer, self._parent)
        # self.help = SettingsButton()
        # self.help.clicked.connect(self.gotoHelpPage)
        # self.layout.addWidget(self.help)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.machine.setText(self.tr("Machine Configuration"))
        self.wlan.setText(self.tr("WLAN"))
        self.theme.setText(self.tr("Theme"))
        self.theme.setTips(self.tr("Light"))
        self.language.setText(self.tr("Language"))
        self.user_manual.setText(self.tr("User manual"))
        self.about.setText(self.tr("About"))
        self.help.setText(self.tr("Help"))
        self.restore_factory.setText(self.tr("Reset"))
        self.nozzle.setText(self.tr("Replace Nozzle Assembly"))

        if self._printer.config.get_language() == 'Chinese':
            self.language.setTips(self.tr("Chinese"))
        elif self._printer.config.get_language() == 'English':
            self.language.setTips(self.tr("English"))

    @pyqtSlot()
    def gotoLanguagePage(self):
        self._parent.gotoPage(self.languagePage, self.tr("Language"))

    @pyqtSlot()
    def gotoAboutPage(self):
        self._parent.gotoPage(self.aboutPage, self.tr("About"))

    # @pyqtSlot()
    # def gotoHelpPage(self):
    #     self._parent.gotoPage(self.helpPage, self.tr("Help"))

    @pyqtSlot()
    def gotoWLANPage(self):
        self._parent.gotoPage(self.wlanPage, self.tr("WLAN"))

    @pyqtSlot()
    def gotoMachinePage(self):
        self._parent.gotoPage(self.machinePage, self.tr("Machine Configuration"))

    @pyqtSlot()
    def gotoNozzlePage(self):
        self._parent.gotoPage(self.nozzlePage, self.tr("Replace Nozzle Assembly"))

    @pyqtSlot()
    def on_restore_factory_clicked(self):
        self._parent.gotoPage(self.resetPage, self.restore_factory.text())
