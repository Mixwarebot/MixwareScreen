import typing

from qtCore import *
from ui.components.messageBar import MessageBar


class BaseTitleFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("frameBox")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(0)

        # self._title = QLabel("title")
        # self._title.setObjectName("title")
        # self._title.setProperty("type", "normal")
        # self._layout.addWidget(self._title)

        self._body_frame = QFrame()
        self._body_frame.setObjectName("frameBox")
        self._body_frame_layout = QVBoxLayout(self._body_frame)
        self._body_frame_layout.setContentsMargins(0, 0, 0, 0)
        self._body_frame_layout.setSpacing(10)

        self._layout.addWidget(self._body_frame)

    # def set_title(self, a0: str):
    #     self._title.setText(a0)

    # def set_layout(self, layout: QLayout):
    #     self._body_frame.setLayout(layout)

    # def get_sub_frame(self):
    #     return self._body_frame

    # def add_message(self, a0: QWidget):
    #     self._body_frame_layout.addWidget(a0)

    def set_message(self, text_list):
        _list = []
        for i in range(len(text_list)):
            _list.append(MessageBar(i + 1, text_list[i]))
            self._body_frame_layout.addWidget(_list[i])

        return _list
