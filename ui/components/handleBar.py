from qtCore import *
from ui.components.base.baseLine import BaseVLine, BaseHLine
from ui.components.base.basePushButton import BasePushButton


class HandleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.body = QFrame(self)
        self.layout.addWidget(self.body)

        self.layout.addWidget(BaseHLine())

        self.footer = QFrame(self)
        self.footer.setFixedHeight(64)
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(0)
        self.previous_button = BasePushButton()
        self.footer_layout.addWidget(self.previous_button)
        self.footer_line = BaseVLine()
        self.footer_layout.addWidget(self.footer_line)
        self.next_button = BasePushButton()
        self.footer_layout.addWidget(self.next_button)
        self.layout.addWidget(self.footer)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()
        if not self.previous_button.isVisible() or not self.next_button.isVisible():
            self.footer_line.hide()

    def re_translate_ui(self):
        self.previous_button.setText(self.tr("Previous"))
        self.next_button.setText(self.tr("Next"))
