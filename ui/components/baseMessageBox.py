import logging

from qtCore import *
from ui.components.base.baseLine import BaseVLine, BaseHLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.base.baseRound import BaseRoundDialog


class BaseMessageBox(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.resize(self._width - 40, self._height / 3)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; }")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")

        self.title_frame_layout = QHBoxLayout(self.title_frame)
        self.title_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.title_frame_layout.setSpacing(0)

        self.title_label = QLabel()
        self.title_frame_layout.addWidget(self.title_label)

        self.title_close_button = BasePushButton()
        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.clicked.connect(self.on_cancel)
        self.title_frame_layout.addWidget(self.title_close_button)
        self.frame_layout.addWidget(self.title_frame)

        self.body_frame = QFrame()
        self.body_frame_layout = QVBoxLayout(self.body_frame)
        self.body_frame_layout.setAlignment(Qt.AlignCenter)
        self.body_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.body_frame_layout.setSpacing(10)
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(210, 210)
        self.body_frame_layout.addWidget(self.logo_label)
        self.message_label = QLabel()
        self.message_label.setObjectName("message")
        self.message_label.setWordWrap(True)
        self.body_frame_layout.addWidget(self.message_label)
        self.frame_layout.addWidget(self.body_frame)
        self.frame_layout.addWidget(BaseHLine())
        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(64)
        self.button_frame_layout = QHBoxLayout(self.footer_frame)
        self.button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.button_frame_layout.setSpacing(0)
        self.cancel_button = BasePushButton()
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_frame_layout.addWidget(self.cancel_button, 1)
        self.button_line = BaseVLine()
        self.button_frame_layout.addWidget(self.button_line)
        self.confirm_button = BasePushButton()
        self.confirm_button.clicked.connect(self.on_confirm)
        self.button_frame_layout.addWidget(self.confirm_button, 1)
        self.frame_layout.addWidget(self.footer_frame)
        self.layout.addWidget(self.frame)

        self.logo_label.hide()

        self.re_translate_ui()

    def re_translate_ui(self):
        self.confirm_button.setText(self.tr("Confirm"))
        self.cancel_button.setText(self.tr("Cancel"))

    def on_confirm(self):
        self.done(QMessageBox.Yes)

    def on_cancel(self):
        self.done(QMessageBox.Cancel)

    def setTitle(self, title: str):
        self.title_label.setText(title)

    def setText(self, text: str):
        self.message_label.setText(text)

    def start(self, title="", text="", image='', align=Qt.AlignCenter, buttons=QMessageBox.NoButton) -> int:
        self.setTitle(title)
        if text == "Restart the printer?":
            text = self.tr("Restart the printer?")
        self.setText(text)
        self.logo_label.hide()

        if image and image != '':
            try:
                file_icon = QPixmap(image)
                self.logo_label.setPixmap(file_icon.scaledToWidth(210))
                if self.logo_label.isHidden():
                    self.logo_label.show()
            except Exception as e:
                logging.info(str(e))

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
