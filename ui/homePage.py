from qtCore import *
from ui.base.basePushButton import BasePushButton


class HomePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("homePage")

        self.homeAllButton = BasePushButton()
        self.homeXButton = BasePushButton()
        self.homeYButton = BasePushButton()
        self.homeZButton = BasePushButton()
        self.disableButton = BasePushButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.homeAllButton.setText(self.tr("Home All"))
        self.homeXButton.setText(self.tr("Home X"))
        self.homeYButton.setText(self.tr("Home Y"))
        self.homeZButton.setText(self.tr("Home Z"))
        self.disableButton.setText(self.tr("Disable Steppers"))

        self.homeAllButton.setObjectName("allButton")
        self.homeXButton.setObjectName("xButton")
        self.homeYButton.setObjectName("yButton")
        self.homeZButton.setObjectName("zButton")
        self.disableButton.setObjectName("disableButton")

        self.homeAllButton.setFixedHeight(64)
        self.homeXButton.setFixedHeight(64)
        self.homeYButton.setFixedHeight(64)
        self.homeZButton.setFixedHeight(64)
        self.disableButton.setFixedHeight(64)

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        layout.addWidget(self.homeAllButton)
        layout.addWidget(self.homeXButton)
        layout.addWidget(self.homeYButton)
        layout.addWidget(self.homeZButton)
        layout.addWidget(self.disableButton)

    def initConnect(self):
        self.homeAllButton.clicked.connect(self.homeAll)
        self.homeXButton.clicked.connect(self.homeX)
        self.homeYButton.clicked.connect(self.homeY)
        self.homeZButton.clicked.connect(self.homeZ)
        self.disableButton.clicked.connect(self.disableSteppers)

    @pyqtSlot()
    def homeAll(self):
        self._printer.write_gcode_command("G28")

    @pyqtSlot()
    def homeX(self):
        self._printer.write_gcode_command("G28X")

    @pyqtSlot()
    def homeY(self):
        self._printer.write_gcode_command("G28Y")

    @pyqtSlot()
    def homeZ(self):
        self._printer.write_gcode_command("G28Z")

    @pyqtSlot()
    def disableSteppers(self):
        self._printer.write_gcode_command("M84")
