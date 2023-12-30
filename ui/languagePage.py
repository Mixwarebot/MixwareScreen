from qtCore import *


class LanguagePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("languagePage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 10)
        self.layout.setSpacing(10)

        self.layout.setAlignment(Qt.AlignTop)
        self.language_e = QPushButton()
        self.language_e.setFixedHeight(64)
        self.language_e.clicked.connect(self.on_language_e_clicked)
        self.layout.addWidget(self.language_e)
        self.language_c = QPushButton()
        self.language_c.setFixedHeight(64)
        self.language_c.clicked.connect(self.on_language_c_clicked)
        self.layout.addWidget(self.language_c)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.language_e.setText(self.tr("English"))
        self.language_c.setText(self.tr("Chinese"))

        if self._printer.config.get_language() == 'English':
            update_style(self.language_e, "checked")
            update_style(self.language_c, "unchecked")
        elif self._printer.config.get_language() == 'Chinese':
            update_style(self.language_e, "unchecked")
            update_style(self.language_c, "checked")

    @pyqtSlot()
    def on_language_e_clicked(self):
        if self._printer.config.get_language() == 'Chinese':
            self._parent.updateTranslator.emit("English")
            update_style(self.language_e, "checked")
            update_style(self.language_c, "unchecked")
            self._parent.gotoMainPage()

    @pyqtSlot()
    def on_language_c_clicked(self):
        if self._printer.config.get_language() == 'English':
            self._parent.updateTranslator.emit("Chinese")
            update_style(self.language_e, "unchecked")
            update_style(self.language_c, "checked")
            self._parent.gotoMainPage()
