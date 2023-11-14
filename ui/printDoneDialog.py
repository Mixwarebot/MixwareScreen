from qtCore import *
from ui.base.baseLine import BaseVLine, BaseHLine
from ui.base.basePushButton import BasePushButton
from ui.base.baseRound import BaseRoundDialog


class PrintDoneDialog(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.resize(self._width - 40, self._height / 3)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; }")
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")
        title_frame_layout = QHBoxLayout(self.title_frame)
        title_frame_layout.setContentsMargins(0, 0, 0, 0)
        title_frame_layout.setSpacing(0)
        self.title_label = QLabel()
        title_frame_layout.addWidget(self.title_label)
        self.title_close_button = BasePushButton()
        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.clicked.connect(self.on_confirm)
        title_frame_layout.addWidget(self.title_close_button)
        frame_layout.addWidget(self.title_frame)

        self.body_frame = QFrame()
        self.body_frame_layout = QVBoxLayout(self.body_frame)
        self.body_frame_layout.setAlignment(Qt.AlignCenter)
        self.body_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.body_frame_layout.setSpacing(0)
        self.message_label = QLabel()
        self.message_label.setObjectName("message")
        self.message_label.setWordWrap(True)
        self.body_frame_layout.addWidget(self.message_label)
        frame_layout.addWidget(self.body_frame)
        frame_layout.addWidget(BaseHLine())

        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(64)
        button_frame_layout = QHBoxLayout(self.footer_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        self.again_button = BasePushButton()
        self.again_button.clicked.connect(self.on_again)
        button_frame_layout.addWidget(self.again_button, 1)
        button_frame_layout.addWidget(BaseVLine())
        self.confirm_button = BasePushButton()
        self.confirm_button.clicked.connect(self.on_confirm)
        button_frame_layout.addWidget(self.confirm_button, 1)
        frame_layout.addWidget(self.footer_frame)

        layout.addWidget(self.frame)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.again_button.setText(self.tr("Print Again"))
        self.confirm_button.setText(self.tr("Confirm"))

    def on_confirm(self):
        self.done(QMessageBox.Cancel)

    def on_again(self):
        self.done(QMessageBox.Yes)

    def setTitle(self, title: str):
        self.title_label.setText(title)

    def setText(self, text: str):
        self.message_label.setText(text)

    def start(self, title="", text="") -> int:
        self.setTitle(title)
        self.setText(text)
        self.message_label.setAlignment(Qt.AlignCenter)

        return self.exec()