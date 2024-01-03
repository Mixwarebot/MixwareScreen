from qtCore import *
from ui.settingsButton import SettingsButton


class FeedRatePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("feedRatePage")

        self.feed_rate_x = SettingsButton()
        self.feed_rate_y = SettingsButton()
        self.feed_rate_z = SettingsButton()
        self.feed_rate_e = SettingsButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.reTranslateUi()

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.feed_rate_x)
        layout.addWidget(self.feed_rate_y)
        layout.addWidget(self.feed_rate_z)
        layout.addWidget(self.feed_rate_e)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.feed_rate_x.clicked.connect(self.on_feed_rate_x_clicked)
        self.feed_rate_y.clicked.connect(self.on_feed_rate_y_clicked)
        self.feed_rate_z.clicked.connect(self.on_feed_rate_z_clicked)
        self.feed_rate_e.clicked.connect(self.on_feed_rate_e_clicked)

    @pyqtSlot()
    def on_feed_rate_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.feed_rate_x.text()}: {self.feed_rate_x.tips()}", "feed_rate_x")

    @pyqtSlot()
    def on_feed_rate_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.feed_rate_y.text()}: {self.feed_rate_y.tips()}", "feed_rate_y")

    @pyqtSlot()
    def on_feed_rate_z_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.feed_rate_z.text()}: {self.feed_rate_z.tips()}", "feed_rate_z")

    @pyqtSlot()
    def on_feed_rate_e_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.feed_rate_e.text()}: {self.feed_rate_e.tips()}", "feed_rate_e")

    def onUpdatePrinterInformation(self):
        self.reTranslateUi()

    def reTranslateUi(self):
        self.feed_rate_x.setText(self.tr("X-Axis Maximum Feed Rate"))
        self.feed_rate_y.setText(self.tr("Y-Axis Maximum Feed Rate"))
        self.feed_rate_z.setText(self.tr("Z-Axis Maximum Feed Rate"))
        self.feed_rate_e.setText(self.tr("E-Axis Maximum Feed Rate"))

        self.feed_rate_x.setTips(f"{self._printer.information['motor']['maxFeedRate']['X']}")
        self.feed_rate_y.setTips(f"{self._printer.information['motor']['maxFeedRate']['Y']}")
        self.feed_rate_z.setTips(f"{self._printer.information['motor']['maxFeedRate']['Z']}")
        self.feed_rate_e.setTips(f"{self._printer.information['motor']['maxFeedRate']['E']}")

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()
