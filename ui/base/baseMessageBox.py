from qtCore import *
from ui.base.baseLine import BaseVLine, BaseHLine
from ui.base.basePushButton import BasePushButton
from ui.base.baseRound import BaseRoundDialog


class BaseMessageBox(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.frame = QFrame()

        self.title_frame = QFrame()
        self.title_label = QLabel()
        self.title_close_button = BasePushButton()

        self.body_frame = QFrame()
        self.body_frame_layout = QVBoxLayout(self.body_frame)
        self.message_label = QLabel()

        self.footer_frame = QFrame()
        self.confirm_button = BasePushButton()
        self.button_line = BaseVLine()
        self.cancel_button = BasePushButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.resize(self._width - 40, self._height / 3)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; }")

        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")

        self.footer_frame.setFixedHeight(64)

        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)

        self.body_frame_layout.setAlignment(Qt.AlignCenter)
        self.body_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.body_frame_layout.setSpacing(0)
        self.message_label.setObjectName("message")
        self.message_label.setWordWrap(True)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.confirm_button.setText(self.tr("Confirm"))
        self.cancel_button.setText(self.tr("Cancel"))

    def initLayout(self):
        title_frame_layout = QHBoxLayout(self.title_frame)
        title_frame_layout.setContentsMargins(0, 0, 0, 0)
        title_frame_layout.setSpacing(0)
        title_frame_layout.addWidget(self.title_label)
        title_frame_layout.addWidget(self.title_close_button)

        self.body_frame_layout.addWidget(self.message_label)

        button_frame_layout = QHBoxLayout(self.footer_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        button_frame_layout.addWidget(self.cancel_button, 1)
        button_frame_layout.addWidget(self.button_line)
        button_frame_layout.addWidget(self.confirm_button, 1)

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        frame_layout.addWidget(self.title_frame)
        frame_layout.addWidget(self.body_frame)
        frame_layout.addWidget(BaseHLine())
        frame_layout.addWidget(self.footer_frame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.frame)

    # def addWidget(self, a0: QWidget, stretch: int = 0, alignment: Qt.AlignmentFlag = Qt.Alignment()):
    #     self.body_frame_layout.addWidget(a0, stretch, alignment)

    def initConnect(self):
        self.title_close_button.clicked.connect(self.on_cancel)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.confirm_button.clicked.connect(self.on_confirm)

    def on_confirm(self):
        self.done(QMessageBox.Yes)

    def on_cancel(self):
        self.done(QMessageBox.Cancel)

    def setTitle(self, title: str):
        self.title_label.setText(title)

    def setText(self, text: str):
        self.message_label.setText(text)

    def start(self, title="", text="", align=Qt.AlignCenter, buttons=QMessageBox.NoButton) -> int:
        self.setTitle(title)
        self.setText(text)

        self.message_label.setAlignment(align)

        if buttons == QMessageBox.NoButton:
            self.footer_frame.hide()
        elif buttons == QMessageBox.Yes:
            self.footer_frame.show()
            self.cancel_button.hide()
            self.button_line.hide()
            self.confirm_button.show()
        elif buttons == QMessageBox.Cancel:
            self.footer_frame.show()
            self.cancel_button.show()
            self.button_line.hide()
            self.confirm_button.hide()
        elif buttons == QMessageBox.Yes | QMessageBox.Cancel:
            self.footer_frame.show()
            self.cancel_button.show()
            self.button_line.show()
            self.confirm_button.show()

        self.re_translate_ui()
        return self.exec()