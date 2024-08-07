from qtCore import *
from ui.components.base.baseLine import BaseVLine, BaseHLine
from ui.components.base.basePushButton import BasePushButton


class OffsetPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent
        self.offset = {
            'left': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
            'right': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        }

        self.setObjectName("offsetPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(20, 20, 20, 20)
        self.frame_layout.setSpacing(20)

        self.distance_layout = QVBoxLayout()
        self.distance_layout.setContentsMargins(0, 0, 0, 0)
        self.distance_layout.setSpacing(0)
        self.distance_title = QLabel()
        self.distance_title.setObjectName("frame_title")
        self.distance_title.setFixedHeight(40)
        self.distance_layout.addWidget(self.distance_title)
        self.distance_frame = QFrame()
        self.distance_frame.setObjectName("frameOutLine")
        self.distance_frame.setFixedHeight(88)
        self.distance_frame_layout = QHBoxLayout(self.distance_frame)
        self.distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.distance_frame_layout.setSpacing(0)
        self.offset_distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self.offset_distance_default = "0.1"
        self.offset_distance_current_id = 0
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked.connect(self.on_button_clicked)
        for d in range(len(self.offset_distance_list)):
            button = BasePushButton()
            button.setText(self.offset_distance_list[d])
            self.button_group.addButton(button, d)
            if self.offset_distance_list[d] == self.offset_distance_default:
                self.on_button_clicked(self.button_group.button(d))
            self.distance_frame_layout.addWidget(button)
        self.distance_layout.addWidget(self.distance_frame)
        self.frame_layout.addLayout(self.distance_layout, 1)

        self.axis_frame_layout = QVBoxLayout()
        self.axis_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.axis_frame_layout.setSpacing(20)
        self.x_frame_layout = QVBoxLayout()
        self.x_frame_layout.setSpacing(0)
        self.x_frame_title = QLabel()
        self.x_frame_title.setObjectName("frame_title")
        self.x_frame_title.setFixedHeight(40)
        self.x_frame_layout.addWidget(self.x_frame_title)
        self.x_button_frame = QFrame()
        self.x_button_frame.setObjectName("frameOutLine")
        self.x_button_frame_layout = QVBoxLayout(self.x_button_frame)
        self.x_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.x_button_frame_layout.setSpacing(0)
        self.x_button_frame_top_layout = QHBoxLayout()
        self.x_left_button = BasePushButton()
        self.x_left_button.setObjectName("extruderButton")
        self.x_left_button.setFixedHeight(64)
        self.button_group.addButton(self.x_left_button)
        self.x_button_frame_top_layout.addWidget(self.x_left_button)
        self.x_right_button = BasePushButton()
        self.x_right_button.setObjectName("extruderButton")
        self.x_right_button.setFixedHeight(64)
        self.button_group.addButton(self.x_right_button)
        self.x_button_frame_top_layout.addWidget(self.x_right_button)
        self.x_button_frame_layout.addLayout(self.x_button_frame_top_layout)
        self.x_button_frame_layout.addWidget(BaseHLine())
        self.x_button_frame_bottom_layout = QHBoxLayout()
        self.x_dec_button = BasePushButton()
        self.x_dec_button.setObjectName("leftLogo")
        self.x_dec_button.clicked.connect(self.on_x_dec_button_clicked)
        self.x_button_frame_bottom_layout.addWidget(self.x_dec_button)
        self.x_button_frame_bottom_layout.addWidget(BaseVLine())
        self.x_add_button = BasePushButton()
        self.x_add_button.setObjectName("rightLogo")
        self.x_add_button.clicked.connect(self.on_x_add_button_clicked)
        self.x_button_frame_bottom_layout.addWidget(self.x_add_button)
        self.x_button_frame_layout.addLayout(self.x_button_frame_bottom_layout)
        self.x_frame_layout.addWidget(self.x_button_frame)
        self.axis_frame_layout.addLayout(self.x_frame_layout, 4)
        self.yz_frame_layout = QHBoxLayout()
        self.yz_frame_layout.setSpacing(10)
        self.y_frame_layout = QVBoxLayout()
        self.y_frame_layout.setSpacing(0)
        self.y_frame_title = QLabel()
        self.y_frame_title.setObjectName("frame_title")
        self.y_frame_title.setFixedHeight(40)
        self.y_frame_layout.addWidget(self.y_frame_title)
        self.y_button_frame = QFrame()
        self.y_button_frame.setObjectName("frameOutLine")
        self.y_button_frame_layout = QVBoxLayout(self.y_button_frame)
        self.y_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.y_button_frame_layout.setSpacing(0)
        self.y_dec_button = BasePushButton()
        self.y_dec_button.setObjectName("upLogo")
        self.y_dec_button.clicked.connect(self.on_y_dec_button_clicked)
        self.y_button_frame_layout.addWidget(self.y_dec_button)
        self.y_button_frame_layout.addWidget(BaseHLine())
        self.y_add_button = BasePushButton()
        self.y_add_button.setObjectName("downLogo")
        self.y_add_button.clicked.connect(self.on_y_add_button_clicked)
        self.y_button_frame_layout.addWidget(self.y_add_button)
        self.y_frame_layout.addWidget(self.y_button_frame)
        self.yz_frame_layout.addLayout(self.y_frame_layout)
        self.z_frame_layout = QVBoxLayout()
        self.z_frame_layout.setSpacing(0)
        self.z_frame_title = QLabel()
        self.z_frame_title.setObjectName("frame_title")
        self.z_frame_title.setFixedHeight(40)
        self.z_frame_layout.addWidget(self.z_frame_title)
        self.z_button_frame = QFrame()
        self.z_button_frame.setObjectName("frameOutLine")
        self.z_button_frame_layout = QVBoxLayout(self.z_button_frame)
        self.z_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.z_button_frame_layout.setSpacing(0)
        self.z_dec_button = BasePushButton()
        self.z_dec_button.setObjectName("upLogo")
        self.z_dec_button.clicked.connect(self.on_z_dec_button_clicked)
        self.z_button_frame_layout.addWidget(self.z_dec_button)
        self.z_button_frame_layout.addWidget(BaseHLine())
        self.z_add_button = BasePushButton()
        self.z_add_button.setObjectName("downLogo")
        self.z_add_button.clicked.connect(self.on_z_add_button_clicked)
        self.z_button_frame_layout.addWidget(self.z_add_button)
        self.z_frame_layout.addWidget(self.z_button_frame)
        self.yz_frame_layout.addLayout(self.z_frame_layout)
        self.axis_frame_layout.addLayout(self.yz_frame_layout, 5)
        self.frame_layout.addLayout(self.axis_frame_layout, 5)
        self.save_button = BasePushButton()
        self.save_button.setMaximumHeight(88)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.save_button.setStyleSheet("border: 1px solid #D4D4D4; border-radius: 10px")
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.frame_layout.addWidget(self.save_button, 1)
        self.layout.addWidget(self.frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self._printer.write_gcode_command("M851\nM218")
        self.re_translate_ui()
        self.offset['left']['X'] = self._printer.information['probe']['offset']['left']['X']
        self.offset['left']['Y'] = self._printer.information['probe']['offset']['left']['Y']
        self.offset['left']['Z'] = self._printer.information['probe']['offset']['left']['Z']
        self.offset['right']['X'] = self._printer.information['probe']['offset']['right']['X']
        self.offset['right']['Y'] = self._printer.information['probe']['offset']['right']['Y']
        self.offset['right']['Z'] = self._printer.information['probe']['offset']['right']['Z']
        self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y160 F8400\nG1 Z0 F320")

    def hideEvent(self, a0: QHideEvent) -> None:
        self._printer.write_gcode_commands("G28\nT0\nM84")

    def re_translate_ui(self):
        self.x_left_button.setText(self.tr("Left"))
        self.x_right_button.setText(self.tr("Right"))
        self.x_frame_title.setText("X: -")
        self.y_frame_title.setText("Y: -")
        self.z_frame_title.setText("Z: -")
        self.distance_title.setText(self.tr("Move Distance (mm)"))
        self.save_button.setText(self.tr("Save"))
        self.x_dec_button.setTitle(self.tr("Move\nLeft"))
        self.x_add_button.setTitle(self.tr("Move\nRight"))
        self.y_dec_button.setTitle(self.tr("Move\nBack"))
        self.y_add_button.setTitle(self.tr("Move\nForward"))
        self.z_dec_button.setTitle(self.tr("Lift\nBed"))
        self.z_add_button.setTitle(self.tr("Drop\nBed"))

    @pyqtSlot()
    def on_x_dec_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['X'] -= float(self.offset_distance_list[self.offset_distance_current_id])
            self.x_frame_title.setText(
                f"X: {self.offset['left']['X']:.2f}({self._printer.information['probe']['offset']['left']['X']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['X'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.x_frame_title.setText(
                f"X: {self.offset['right']['X']:.2f}({self._printer.information['probe']['offset']['right']['X']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 X-{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot()
    def on_x_add_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['X'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.x_frame_title.setText(
                f"X: {self.offset['left']['X']:.2f}({self._printer.information['probe']['offset']['left']['X']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['X'] -= float(self.offset_distance_list[self.offset_distance_current_id])
            self.x_frame_title.setText(
                f"X: {self.offset['right']['X']:.2f}({self._printer.information['probe']['offset']['right']['X']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 X{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot()
    def on_y_dec_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['Y'] -= float(self.offset_distance_list[self.offset_distance_current_id])
            self.y_frame_title.setText(
                f"Y: {self.offset['left']['Y']:.2f}({self._printer.information['probe']['offset']['left']['Y']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['Y'] -= float(self.offset_distance_list[self.offset_distance_current_id])
            self.y_frame_title.setText(
                f"Y: {self.offset['right']['Y']:.2f}({self._printer.information['probe']['offset']['right']['Y']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 Y-{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot()
    def on_y_add_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['Y'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.y_frame_title.setText(
                f"Y: {self.offset['left']['Y']:.2f}({self._printer.information['probe']['offset']['left']['Y']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['Y'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.y_frame_title.setText(
                f"Y: {self.offset['right']['Y']:.2f}({self._printer.information['probe']['offset']['right']['Y']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 Y{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot()
    def on_z_dec_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['Z'] -= float(self.offset_distance_list[self.offset_distance_current_id])
            self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
            self.z_frame_title.setText(
                f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['Z'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.offset['right']['Z'] = float('%.2f' % self.offset['right']['Z'])
            self.z_frame_title.setText(
                f"Z: {self.offset['right']['Z']:.2f}({self._printer.information['probe']['offset']['right']['Z']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 Z-{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot()
    def on_z_add_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self.offset['left']['Z'] += float(self.offset_distance_list[self.offset_distance_current_id])
            self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
            self.z_frame_title.setText(
                f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")
        elif self._printer.get_extruder() == "right":
            self.offset['right']['Z'] -= float(
                '%.2f' % float(self.offset_distance_list[self.offset_distance_current_id]))
            self.offset['right']['Z'] = float('%.2f' % self.offset['right']['Z'])
            self.z_frame_title.setText(
                f"Z: {self.offset['right']['Z']:.2f}({self._printer.information['probe']['offset']['right']['Z']:.2f})")
        self._printer.write_gcode_command(
            f"G91\nG0 F600 Z{self.offset_distance_list[self.offset_distance_current_id]}\nG90")

    @pyqtSlot(QAbstractButton)
    def on_button_clicked(self, button):
        if button.text() == self.tr("Left"):
            if self._printer.get_extruder() == "right":
                self._printer.write_gcode_commands("G28\nT0\nG1 Y160 Z15 X190 F8400\nG1 Z0 F320")
                self.offset['right']['X'] = self._printer.information['probe']['offset']['right']['X']
                self.offset['right']['Y'] = self._printer.information['probe']['offset']['right']['Y']
                self.offset['right']['Z'] = self._printer.information['probe']['offset']['right']['Z']
        elif button.text() == self.tr("Right"):
            if self._printer.get_extruder() == "left":
                self._printer.write_gcode_commands("G28\nT1\nG1 Y160 Z15 X190 F8400\nG1 Z0 F320")
                self.offset['left']['X'] = self._printer.information['probe']['offset']['left']['X']
                self.offset['left']['Y'] = self._printer.information['probe']['offset']['left']['Y']
                self.offset['left']['Z'] = self._printer.information['probe']['offset']['left']['Z']
        elif button.text() in self.offset_distance_list:
            if self.button_group.id(button) != self.offset_distance_current_id:
                update_style(self.button_group.button(self.offset_distance_current_id), "unchecked")
                update_style(self.button_group.button(self.button_group.id(button)), "checked")
                self.offset_distance_current_id = self.button_group.id(button)

    def on_save_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_commands(
                f"M851 X{self.offset['left']['X']:.2f} Y{self.offset['left']['Y']:.2f} Z{self.offset['left']['Z']:.2f}\nM500\nM851")
        elif self._printer.get_extruder() == "right":
            self._printer.write_gcode_commands(
                f"M218 T1 X{self.offset['right']['X']:.2f} Y{self.offset['right']['Y']:.2f} Z{self.offset['right']['Z']:.2f}\nM500\nM218")

    def on_update_printer_information(self):
        if not self.isVisible():
            return
        if self._printer.get_extruder() == "left":
            update_style(self.x_left_button, "checked")
            update_style(self.x_right_button, "unchecked")
            self.x_frame_title.setText(
                f"X: {self.offset['left']['X']:.2f}({self._printer.information['probe']['offset']['left']['X']:.2f})")
            self.y_frame_title.setText(
                f"Y: {self.offset['left']['Y']:.2f}({self._printer.information['probe']['offset']['left']['Y']:.2f})")
            self.z_frame_title.setText(
                f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")
        elif self._printer.get_extruder() == "right":
            update_style(self.x_left_button, "unchecked")
            update_style(self.x_right_button, "checked")
            self.x_frame_title.setText(
                f"X: {self.offset['right']['X']:.2f}({self._printer.information['probe']['offset']['right']['X']:.2f})")
            self.y_frame_title.setText(
                f"Y: {self.offset['right']['Y']:.2f}({self._printer.information['probe']['offset']['right']['Y']:.2f})")
            self.z_frame_title.setText(
                f"Z: {self.offset['right']['Z']:.2f}({self._printer.information['probe']['offset']['right']['Z']:.2f})")
