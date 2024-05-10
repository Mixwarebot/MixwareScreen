import typing

from qtCore import *


class BaseTitleFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("frameBox")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 3, 0, 10)
        self._layout.setSpacing(0)

        self._title = QLabel("title")
        self._title.setObjectName("title")
        self._title.setProperty("titleType", "normal")
        self._layout.addWidget(self._title)

        self._body_frame = QFrame()
        self._body_frame.setObjectName("frameBox")

        self._layout.addWidget(self._body_frame)

    def set_title(self, a0: str):
        self._title.setText(a0)

    def set_layout(self, layout: QLayout):
        self._body_frame.setLayout(layout)
