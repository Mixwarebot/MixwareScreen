from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.pages.leveling.levelPage import LevelPage
from ui.pages.leveling.levelWizardPage import LevelWizardPage


class LevelPreParePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("levelPreParePage")

        self.button_layout = QVBoxLayout(self)
        self.button_layout.setContentsMargins(20, 0, 20, 0)
        self.button_layout.setSpacing(10)

        self.wizard_button = BasePushButton()
        self.wizard_button.clicked.connect(self.goto_level_wizard_page)
        self.button_layout.addWidget(self.wizard_button)
        self.custom_button = BasePushButton()
        self.custom_button.clicked.connect(self.goto_level_page)
        self.button_layout.addWidget(self.custom_button)

        self.wizardPage = LevelWizardPage(self._printer, self._parent)
        self.levelPage = LevelPage(self._printer, self._parent)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.wizard_button.setText(self.tr("Leveling Wizard"))
        self.custom_button.setText(self.tr("Customize Leveling"))

    @pyqtSlot()
    def goto_level_wizard_page(self):
        self._parent.gotoPage(self.wizardPage, self.tr("Leveling Wizard"))

    @pyqtSlot()
    def goto_level_page(self):
        self._parent.gotoPage(self.levelPage, self.tr("Level"))
