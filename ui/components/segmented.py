from qtCore import *


class Segmented(QFrame):
    clicked = pyqtSignal()

    def __init__(self, options=None, default_value=None, on_change=None, parent=None):
        super().__init__(parent)
        if options is None:
            options = []
        if default_value is None:
            default_value = options[0]

        self._options = options
        self._default_value = default_value
        self._value = default_value
        self._on_change = on_change
        self._current_id = 0

        self.setObjectName("frameBox")
        self.setFixedHeight(88)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(1, 1, 1, 1)
        self._layout.setSpacing(0)

        self.items_group = QButtonGroup()
        self.items_group.buttonClicked.connect(self.on_items_group_clicked)
        for i in range(len(self._options)):
            button = QPushButton()
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setText(str(self._options[i]))
            self.items_group.addButton(button, i)
            if self._options[i] == self._default_value:
                self.on_items_group_clicked(self.items_group.button(i))
            self._layout.addWidget(button)

    @property
    def value(self):
        return self._value

    @pyqtSlot(QAbstractButton)
    def on_items_group_clicked(self, button):
        if self.items_group.id(button) != self._current_id:
            update_style(self.items_group.button(self._current_id), "unchecked")
            update_style(button, "checked")
            self._current_id = self.items_group.id(button)
            self._value = button.text()
