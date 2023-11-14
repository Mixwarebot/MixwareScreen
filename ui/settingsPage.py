# from main import installTranslator
from qtCore import *
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

        self.machine = SettingsButton()
        self.wlan = SettingsButton()
        self.theme = SettingsButton()
        self.language = SettingsButton()
        self.about = SettingsButton()

        self.machinePage = MachinePage(self._printer, self._parent)
        self.wlanPage = WlanPage(self._printer, self._parent)
        QScroller.grabGesture(self.wlanPage, QScroller.TouchGesture)
        self.lang = 0

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.machine.setText(self.tr("Machine Configuration"))
        self.wlan.setText(self.tr("WLAN"))
        self.theme.setText(self.tr("Theme"))
        self.theme._tips.setText(self.tr("Light"))
        self.language.setText(self.tr("Language"))
        self.about.setText(self.tr("About"))
        if self._printer.config.get_language() == 'Chinese':
            self.language._tips.setText(self.tr("Chinese"))
        elif self._printer.config.get_language() == 'English':
            self.language._tips.setText(self.tr("English"))

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.machine)
        layout.addWidget(self.wlan)
        layout.addWidget(self.theme)
        layout.addWidget(self.language)
        layout.addWidget(self.about)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self.about.clicked.connect(self.openAboutDialog)
        self.machine.clicked.connect(self.gotoMachinePage)
        self.wlan.clicked.connect(self.gotoWLANPage)
        self.language.clicked.connect(self.trans)

    @pyqtSlot()
    def openAboutDialog(self):
        info = ""
        if self._printer.version():
            info += self.tr("Version: {}\n").format(self._printer.version())
        if "Unknown" not in self._printer.deviceName():
            info += self.tr("Printer Name: {}\n").format(self._printer.deviceName())
            info += self.tr("Printer Version: {}\n").format(self._printer.deviceVersion())
        else:
            info += self.tr("Printer disconnected.\n")
        if self._printer.get_ip_addr("wlan0"):
            info += self.tr("IP Address: {}\n").format(self._printer.get_ip_addr("wlan0"))
        self._parent.showShadowScreen()
        self._parent.message.start(self.tr("About"), info, buttons=QMessageBox.Yes)
        self._parent.closeShadowScreen()

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