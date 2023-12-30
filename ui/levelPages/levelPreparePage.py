from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.levelPages.levelPage import LevelPage
from ui.levelPages.levelWizardPage import LevelWizardPage


class LevelPreParePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("levelPreParePage")

        self.wizard_button = BasePushButton()
        self.custom_button = BasePushButton()

        self.wizardPage = LevelWizardPage(self._printer, self._parent)
        self.levelPage = LevelPage(self._printer, self._parent)

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.wizard_button.setText(self.tr("Leveling Wizard"))
        self.custom_button.setText(self.tr("Customize Leveling"))

    def initLayout(self):
        button_layout = QVBoxLayout(self)
        button_layout.setContentsMargins(20, 0, 20, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.wizard_button)
        button_layout.addWidget(self.custom_button)

    def initConnect(self):
        self.wizard_button.clicked.connect(self.goto_level_wizard_page)
        self.custom_button.clicked.connect(self.goto_level_page)

    @pyqtSlot()
    def goto_level_wizard_page(self):
        self._parent.gotoPage(self.wizardPage, self.tr("Leveling Wizard"))

    @pyqtSlot()
    def goto_level_page(self):
        self._parent.gotoPage(self.levelPage, self.tr("Level"))
