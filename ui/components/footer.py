from qtCore import *
from ui.components.base.basePushButton import BasePushButton


class FooterBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(128)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(30, 18, 30, 26)
        self.layout.setSpacing(10)

        self.reboot_stop_button = BasePushButton()
        self.reboot_stop_button.setObjectName("eStopButton")
        self.reboot_stop_button.setFixedSize(84, 84)
        self.layout.addWidget(self.reboot_stop_button)

        self.mainButton = BasePushButton()
        self.mainButton.setObjectName("mainButton")
        self.mainButton.setFixedHeight(84)
        self.layout.addWidget(self.mainButton)

        self.previousButton = BasePushButton()
        self.previousButton.setObjectName("previousButton")
        self.previousButton.setFixedSize(84, 84)
        self.layout.addWidget(self.previousButton)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.mainButton.setText(self.tr("Main"))
