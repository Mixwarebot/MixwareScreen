from qtCore import *
from ui.base.basePushButton import BasePushButton


class HomePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("homePage")

        self.layout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.homeAllButton = BasePushButton()
        self.homeAllButton.setObjectName("allButton")
        self.homeAllButton.clicked.connect(self.home_all)
        self.layout.addWidget(self.homeAllButton, 0, 0)

        self.homeXButton = BasePushButton()
        self.homeXButton.setObjectName("xButton")
        self.homeXButton.clicked.connect(self.home_x)
        self.layout.addWidget(self.homeXButton, 0, 1)

        self.homeYButton = BasePushButton()
        self.homeYButton.setObjectName("yButton")
        self.homeYButton.clicked.connect(self.home_y)
        self.layout.addWidget(self.homeYButton, 1, 0)

        self.homeZButton = BasePushButton()
        self.homeZButton.setObjectName("zButton")
        self.homeZButton.clicked.connect(self.home_z)
        self.layout.addWidget(self.homeZButton, 1, 1)

        self.disableButton = BasePushButton()
        self.disableButton.setObjectName("disableButton")
        self.disableButton.clicked.connect(self.disable_steppers)
        self.layout.addWidget(self.disableButton, 2, 0)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.homeAllButton.setText(self.tr("Home All"))
        self.homeXButton.setText(self.tr("Home X"))
        self.homeYButton.setText(self.tr("Home Y"))
        self.homeZButton.setText(self.tr("Home Z"))
        self.disableButton.setText(self.tr("Disable Steppers"))

    @pyqtSlot()
    def home_all(self):
        self._printer.write_gcode_command("G28")

    @pyqtSlot()
    def home_x(self):
        self._printer.write_gcode_command("G28X")

    @pyqtSlot()
    def home_y(self):
        self._printer.write_gcode_command("G28Y")

    @pyqtSlot()
    def home_z(self):
        self._printer.write_gcode_command("G28Z")

    @pyqtSlot()
    def disable_steppers(self):
        self._printer.write_gcode_command("M84")
