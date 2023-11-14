from qtCore import *
from ui.base.baseLine import BaseVLine, BaseHLine
from ui.base.basePushButton import BasePushButton


class HandleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.body = QFrame(self)
        self.footer = QFrame(self)
        self.footer.setFixedHeight(64)

        self.previous_button = BasePushButton(self.tr("Previous"))
        self.next_button = BasePushButton(self.tr("Next"))
        self.footer_line = BaseVLine()

        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(0)
        footer_layout.addWidget(self.previous_button)
        footer_layout.addWidget(self.footer_line)
        footer_layout.addWidget(self.next_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.body)
        layout.addWidget(BaseHLine())
        layout.addWidget(self.footer)

    def showEvent(self, a0: QShowEvent) -> None:
        if not self.previous_button.isVisible() or not self.next_button.isVisible():
            self.footer_line.hide()