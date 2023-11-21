# from main import installTranslator
from qtCore import *
from ui.aboutPage import AboutPage
from ui.machinePages.accelerationPage import AccelerationPage
from ui.machinePages.machinePage import MachinePage
from ui.settingsButton import SettingsButton
from ui.wlanPage import WlanPage


class SettingsPage(QWidget):
    new_trans = pyqtSignal(str)
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("settingsPage")

        self.lang = 0

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.machinePage = MachinePage(self._printer, self._parent)
        self.machine = SettingsButton()
        self.machine.clicked.connect(self.gotoMachinePage)
        self.layout.addWidget(self.machine)

        self.wlanPage = WlanPage(self._printer, self._parent)
        QScroller.grabGesture(self.wlanPage, QScroller.TouchGesture)
        self.wlan = SettingsButton()
        self.wlan.clicked.connect(self.gotoWLANPage)
        self.layout.addWidget(self.wlan)

        self.theme = SettingsButton()
        self.layout.addWidget(self.theme)

        self.language = SettingsButton()
        self.language.clicked.connect(self.trans)
        self.layout.addWidget(self.language)

        self.aboutPage = AboutPage(self._printer, self._parent)
        self.about = SettingsButton()
        self.about.clicked.connect(self.gotoAboutPage)
        self.layout.addWidget(self.about)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()


    def re_translate_ui(self):
        self.machine.setText(self.tr("Machine Configuration"))
        self.wlan.setText(self.tr("WLAN"))
        self.theme.setText(self.tr("Theme"))
        self.theme.setTips(self.tr("Light"))
        self.language.setText(self.tr("Language"))
        self.about.setText(self.tr("About"))
        if self._printer.config.get_language() == 'Chinese':
            self.language.setTips(self.tr("Chinese"))
        elif self._printer.config.get_language() == 'English':
            self.language.setTips(self.tr("English"))

        self.theme.hide()
        self.language.hide()

    @pyqtSlot()
    def gotoAboutPage(self):
        self._parent.gotoPage(self.aboutPage, "About")

    @pyqtSlot()
    def gotoWLANPage(self):
        self._parent.gotoPage(self.wlanPage, "WLAN")

    @pyqtSlot()
    def gotoMachinePage(self):
        self._parent.gotoPage(self.machinePage, "Machine Configuration")

    @pyqtSlot()
    def trans(self):
        print(self._printer.config.get_language())
        if self._printer.config.get_language() == 'English':
            self._parent.updateTranslator.emit('Chinese')
            self._printer.config.set_language('Chinese')
        else:
            self._parent.updateTranslator.emit('English')
            self._printer.config.set_language('English')

    def reTranslateUi(self):
        self.machine.setText(self.tr("Machine Configuration"))

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()