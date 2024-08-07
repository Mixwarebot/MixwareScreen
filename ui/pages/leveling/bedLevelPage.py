from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.components.movieLabel import MovieLabel


class BedLevelPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent

        self.setObjectName("bedLevelPage")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.diagram_frame = QFrame()
        self.diagram_frame.setObjectName("frameBox")
        self.diagram_frame_layout = QHBoxLayout(self.diagram_frame)
        self.diagram_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.diagram_frame_layout.setAlignment(Qt.AlignCenter)
        self.diagram_logo = MovieLabel("resource/image/bed_level.gif", 320, 320)
        self.diagram_logo.setFixedSize(320, 320)
        self.diagram_frame_layout.addWidget(self.diagram_logo)
        self.layout.addWidget(self.diagram_frame)

        self.top_layout = QVBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.top_frame_title = QLabel()
        self.top_frame_title.setObjectName("title")
        self.top_frame_title.setProperty("type", "normal")
        self.top_frame_title.setFixedHeight(40)
        self.top_layout.addWidget(self.top_frame_title)

        self.top_frame = QFrame()
        self.top_frame.setObjectName("frameBox")
        self.top_frame.setFixedHeight(66)
        self.top_frame_layout = QHBoxLayout(self.top_frame)
        self.top_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.top_frame_layout.setSpacing(0)
        self.top_frame_layout.setAlignment(Qt.AlignVCenter)
        self.extruder_left_button = QPushButton()
        self.extruder_left_button.setFixedHeight(64)
        self.extruder_left_button.clicked.connect(self.on_left_extruder_button_clicked)
        self.top_frame_layout.addWidget(self.extruder_left_button)
        self.extruder_right_button = QPushButton()
        self.extruder_right_button.setFixedHeight(64)
        self.extruder_right_button.clicked.connect(self.on_right_extruder_button_clicked)
        self.top_frame_layout.addWidget(self.extruder_right_button)
        self.top_layout.addWidget(self.top_frame)
        self.layout.addLayout(self.top_layout)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setFixedSize(self._printer.config.get_width() - 20 - 20, self._printer.config.get_width() - 20 - 20)

        self.left_back_button = QPushButton(self.frame)
        self.left_back_button.clicked.connect(self.on_left_back_button_clicked)
        pix = QPixmap("resource/icon/BLB.png")
        self.left_back_button.setFixedSize(pix.size())
        self.left_back_button.setMask(pix.mask())
        self.left_back_button.setObjectName("leftBackButton")
        self.left_back_button.move(20, 20)

        self.right_back_button = QPushButton(self.frame)
        self.right_back_button.clicked.connect(self.on_right_back_button_clicked)
        pix = QPixmap("resource/icon/BRB.png")
        self.right_back_button.setFixedSize(pix.size())
        self.right_back_button.setMask(pix.mask())
        self.right_back_button.setObjectName("rightBackButton")
        self.right_back_button.move(185, 20)

        self.left_front_button = QPushButton(self.frame)
        self.left_front_button.clicked.connect(self.on_left_front_button_clicked)
        pix = QPixmap("resource/icon/BLF.png")
        self.left_front_button.setFixedSize(pix.size())
        self.left_front_button.setMask(pix.mask())
        self.left_front_button.setObjectName("leftFrontButton")
        self.left_front_button.move(20, 185)

        self.right_front_button = QPushButton(self.frame)
        self.right_front_button.clicked.connect(self.on_right_front_button_clicked)
        pix = QPixmap("resource/icon/BRF.png")
        self.right_front_button.setFixedSize(pix.size())
        self.right_front_button.setMask(pix.mask())
        self.right_front_button.setObjectName("rightFrontButton")
        self.right_front_button.move(185, 185)

        self.center_button = QPushButton(self.frame)
        self.center_button.clicked.connect(self.on_center_button_clicked)
        pix = QPixmap("resource/icon/BCT.png")
        self.center_button.setFixedSize(pix.size())
        self.center_button.setMask(pix.mask())
        self.center_button.setObjectName("centerButton")
        self.center_button.move(93, 93)

        self.layout.addWidget(self.frame)
        self.disable_button = BasePushButton()
        self.disable_button.setFixedHeight(64)
        self.disable_button.clicked.connect(self.on_disable_button_clicked)
        self.layout.addWidget(self.disable_button)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.top_frame_title.setText(self.tr("Current Extruder"))
        self.extruder_left_button.setText(self.tr("Left"))
        self.extruder_right_button.setText(self.tr("Right"))
        self.disable_button.setText(self.tr("Disabled XY"))

    @pyqtSlot()
    def on_left_back_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X20 Y300\nG0 F300 Z0')
        elif self._printer.get_extruder() == "right":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X80 Y300\nG0 F300 Z0')

    @pyqtSlot()
    def on_right_back_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X300 Y300\nG0 F300 Z0')
        elif self._printer.get_extruder() == "right":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X370 Y300\nG0 F300 Z0')

    @pyqtSlot()
    def on_left_front_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X20 Y20\nG0 F300 Z0')
        elif self._printer.get_extruder() == "right":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X80 Y20\nG0 F300 Z0')

    @pyqtSlot()
    def on_right_front_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X300 Y20\nG0 F300 Z0')
        elif self._printer.get_extruder() == "right":
            self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X370 Y20\nG0 F300 Z0')

    @pyqtSlot()
    def on_center_button_clicked(self):
        self._printer.write_gcode_command('G0 F300 Z10\nG0 F4000 X190 Y160\nG0 F300 Z0')

    @pyqtSlot()
    def on_disable_button_clicked(self):
        self._printer.write_gcode_command('M84 XY')

    @pyqtSlot()
    def on_left_extruder_button_clicked(self):
        self._printer.write_gcode_command('T0')

    @pyqtSlot()
    def on_right_extruder_button_clicked(self):
        self._printer.write_gcode_command('T1')

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        if self._printer.get_extruder() == "left":
            update_style(self.extruder_left_button, "checked")
            update_style(self.extruder_right_button, "unchecked")
        elif self._printer.get_extruder() == "right":
            update_style(self.extruder_left_button, "unchecked")
            update_style(self.extruder_right_button, "checked")
