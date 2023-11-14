from qtCore import *
from ui.base.basePushButton import BasePushButton


class FooterBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(128)

        self.mainButton = BasePushButton()
        self.reboot_stop_button = BasePushButton()
        self.previousButton = BasePushButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.mainButton.setText(self.tr("Main"))

        self.reboot_stop_button.setFixedSize(84, 84)
        self.previousButton.setFixedSize(84, 84)
        self.mainButton.setFixedHeight(84)

        self.mainButton.setObjectName("mainButton")
        self.reboot_stop_button.setObjectName("eStopButton")
        self.previousButton.setObjectName("previousButton")

    def initLayout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 18, 30, 26)
        layout.setSpacing(10)
        layout.addWidget(self.reboot_stop_button)
        layout.addWidget(self.mainButton)
        layout.addWidget(self.previousButton)

    def initConnect(self):
        pass