from qtCore import *
from ui.base.baseLine import BaseVLine, BaseHLine
from ui.base.basePushButton import BasePushButton


class MovePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("movePage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(20)

        distance_layout = QVBoxLayout()
        distance_layout.setContentsMargins(0, 0, 0, 0)
        distance_layout.setSpacing(0)

        self.distance_title = QLabel()
        self.distance_title.setObjectName("frame_title")
        self.distance_title.setFixedHeight(40)
        distance_layout.addWidget(self.distance_title)

        self.distance_list = ["0.1", "0.5", "1", "5", "10", "50", "100"]
        self.distance_default = "5"
        self.distance_current_id = 0
        self.distance_frame = QFrame()
        self.distance_frame.setObjectName("frameBox")
        self.distance_frame.setFixedHeight(88)

        distance_frame_layout = QHBoxLayout(self.distance_frame)
        distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        distance_frame_layout.setSpacing(0)

        self.button_group = QButtonGroup()
        self.button_group.buttonClicked.connect(self.on_button_group_clicked)
        for d in range(len(self.distance_list)):
            button = BasePushButton()
            button.setText(self.distance_list[d])
            button.setObjectName("dataButton")
            self.button_group.addButton(button, d)
            if self.distance_list[d] == self.distance_default:
                self.on_button_group_clicked(self.button_group.button(d))
            distance_frame_layout.addWidget(button)
        distance_layout.addWidget(self.distance_frame)
        frame_layout.addLayout(distance_layout, 1)

        frame_midle_layout = QHBoxLayout()
        frame_midle_layout.setContentsMargins(0, 0, 0, 0)

        frame_middle_left_layout = QVBoxLayout()
        frame_middle_left_layout.setContentsMargins(0, 0, 0, 0)
        frame_middle_left_layout.setSpacing(0)

        self.speed_title = QLabel()
        self.speed_title.setFixedHeight(40)
        self.speed_title.setAlignment(Qt.AlignCenter)
        self.speed_title.setStyleSheet("background: transparent; padding: 0;")
        frame_middle_left_layout.addWidget(self.speed_title)

        self.speed_frame = QFrame()
        self.speed_frame.setObjectName("frameBox")
        speed_frame_layout = QVBoxLayout(self.speed_frame)
        speed_frame_layout.setContentsMargins(0, 10, 0, 20)
        speed_frame_layout.setSpacing(10)

        self.speed_label = QLabel()
        self.speed_label.setText("100%")
        self.speed_label.setFixedHeight(40)
        self.speed_label.setAlignment(Qt.AlignCenter)
        speed_frame_layout.addWidget(self.speed_label)

        self.speed_slider = QSlider()
        self.speed_slider.valueChanged.connect(self.on_slider_value_changed)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickPosition(QSlider.TicksRight)
        self.speed_slider.setTickInterval(20)
        self.speed_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        speed_frame_layout.addWidget(self.speed_slider)
        frame_middle_left_layout.addWidget(self.speed_frame)
        frame_middle_left_layout.addSpacing(20)
        self.disabled_button = BasePushButton()
        self.disabled_button.clicked.connect(self.on_disabled_button_clicked)
        self.disabled_button.setMaximumHeight(128)
        self.disabled_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.disabled_button.setStyleSheet("border: 1px solid #D4D4D4; border-radius: 10px")
        frame_middle_left_layout.addWidget(self.disabled_button)
        frame_midle_layout.addLayout(frame_middle_left_layout, 1)
        axis_frame_layout = QVBoxLayout()
        axis_frame_layout.setContentsMargins(0, 0, 0, 0)
        axis_frame_layout.setSpacing(20)

        x_frame_layout = QVBoxLayout()
        x_frame_layout.setSpacing(0)
        self.x_frame_title = QLabel()
        self.x_frame_title.setObjectName("frame_title")
        self.x_frame_title.setFixedHeight(40)
        self.x_frame_title.setText("X: -")
        x_frame_layout.addWidget(self.x_frame_title)
        self.x_button_frame = QFrame()
        self.x_button_frame.setObjectName("frameBox")
        x_button_frame_layout = QVBoxLayout(self.x_button_frame)
        x_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        x_button_frame_layout.setSpacing(0)
        x_button_frame_top_layout = QHBoxLayout()
        self.x_left_button = BasePushButton()
        self.x_left_button.setObjectName("extruderButton")
        self.x_left_button.setFixedHeight(64)
        x_button_frame_top_layout.addWidget(self.x_left_button)
        self.x_right_button = BasePushButton()
        self.x_right_button.setObjectName("extruderButton")
        self.x_right_button.setFixedHeight(64)
        x_button_frame_top_layout.addWidget(self.x_right_button)
        x_button_frame_layout.addLayout(x_button_frame_top_layout)
        x_button_frame_layout.addWidget(BaseHLine())
        x_button_frame_bottom_layout = QHBoxLayout()
        self.x_button_1 = BasePushButton()
        self.x_button_1.setObjectName("leftLogo")
        self.x_button_1.clicked.connect(self.on_x_dec_button_clicked)
        x_button_frame_bottom_layout.addWidget(self.x_button_1)
        x_button_frame_bottom_layout.addWidget(BaseVLine())
        self.x_button_2 = BasePushButton()
        self.x_button_2.setObjectName("rightLogo")
        self.x_button_2.clicked.connect(self.on_x_add_button_clicked)
        x_button_frame_bottom_layout.addWidget(self.x_button_2)
        x_button_frame_layout.addLayout(x_button_frame_bottom_layout)
        x_frame_layout.addWidget(self.x_button_frame)
        axis_frame_layout.addLayout(x_frame_layout, 1)

        axis_frame_layout_2 = QHBoxLayout()
        axis_frame_layout_2.setSpacing(10)

        y_frame_layout = QVBoxLayout()
        y_frame_layout.setSpacing(0)
        self.y_frame_title = QLabel()
        self.y_frame_title.setObjectName("frame_title")
        self.y_frame_title.setFixedHeight(40)
        self.y_frame_title.setText("Y: -")
        y_frame_layout.addWidget(self.y_frame_title)
        self.y_button_frame = QFrame()
        self.y_button_frame.setObjectName("frameBox")
        y_button_frame_layout = QVBoxLayout(self.y_button_frame)
        y_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        y_button_frame_layout.setSpacing(0)
        self.y_button_1 = BasePushButton()
        self.y_button_1.setObjectName("upLogo")
        self.y_button_1.clicked.connect(self.on_y_add_button_clicked)
        y_button_frame_layout.addWidget(self.y_button_1)
        y_button_frame_layout.addWidget(BaseHLine())
        self.y_button_2 = BasePushButton()
        self.y_button_2.setObjectName("downLogo")
        self.y_button_2.clicked.connect(self.on_y_dec_button_clicked)
        y_button_frame_layout.addWidget(self.y_button_2)
        y_frame_layout.addWidget(self.y_button_frame)
        axis_frame_layout_2.addLayout(y_frame_layout)

        z_frame_layout = QVBoxLayout()
        z_frame_layout.setSpacing(0)
        self.z_frame_title = QLabel()
        self.z_frame_title.setObjectName("frame_title")
        self.z_frame_title.setFixedHeight(40)
        self.z_frame_title.setText("Z: -")
        z_frame_layout.addWidget(self.z_frame_title)
        self.z_button_frame = QFrame()
        self.z_button_frame.setObjectName("frameBox")
        z_button_frame_layout = QVBoxLayout(self.z_button_frame)
        z_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        z_button_frame_layout.setSpacing(0)
        self.z_button_1 = BasePushButton()
        self.z_button_1.setObjectName("upLogo")
        self.z_button_1.clicked.connect(self.on_z_dec_button_clicked)
        z_button_frame_layout.addWidget(self.z_button_1)
        z_button_frame_layout.addWidget(BaseHLine())
        self.z_button_2 = BasePushButton()
        self.z_button_2.setObjectName("downLogo")
        self.z_button_2.clicked.connect(self.on_z_add_button_clicked)
        z_button_frame_layout.addWidget(self.z_button_2)
        z_frame_layout.addWidget(self.z_button_frame)
        axis_frame_layout_2.addLayout(z_frame_layout)
        axis_frame_layout.addLayout(axis_frame_layout_2, 1)
        frame_midle_layout.addLayout(axis_frame_layout, 3)
        frame_layout.addLayout(frame_midle_layout, 5)
        self.layout.addWidget(self.frame)

        self.button_group.addButton(self.x_left_button)
        self.button_group.addButton(self.x_right_button)

        self.on_button_group_clicked(self.x_left_button)
        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.x_button_1.setTitle(self.tr("Move\nLeft"))
        self.x_button_2.setTitle(self.tr("Move\nRight"))
        self.y_button_1.setTitle(self.tr("Move\nBack"))
        self.y_button_2.setTitle(self.tr("Move\nForward"))
        self.z_button_1.setTitle(self.tr("Lift\nBed"))
        self.z_button_2.setTitle(self.tr("Drop\nBed"))
        self.x_left_button.setText(self.tr("Left"))
        self.x_right_button.setText(self.tr("Right"))
        self.speed_title.setText(self.tr("Speed"))
        self.distance_title.setText(self.tr("Move Distance (mm)"))
        self.disabled_button.setText(self.tr("Unlock\nMotor"))

    @pyqtSlot()
    def on_slider_value_changed(self):
        self.speed_label.setText(str(self.speed_slider.value()) + '%')

    def move_axis(self, axis: str, pos: float):
        speed = 6000
        if axis == 'X':
            pos += self._printer.get_position('X')
            if self._printer.get_extruder() == 'left':
                if pos < 0:
                    pos = 0
                elif pos > 320:
                    pos = 320
            elif self._printer.get_extruder() == 'right':
                if pos < 60:
                    pos = 60
                elif pos > 385:
                    pos = 385
        elif axis == 'Y':
            pos += self._printer.get_position('Y')
            if pos < 0:
                pos = 0
            elif pos > 320:
                pos = 320
        speed *= self.speed_slider.value() / 100

        if axis == 'Z':
            speed = 720
            pos += self._printer.get_position('Z')
            if pos < 0:
                pos = 0
            elif pos > 400:
                pos = 400
            speed *= self.speed_slider.value() / 100
            if speed > 1000: speed = 1000

        cmd = "G0" + axis + str(pos) + "F" + str(int(speed))
        self._printer.write_gcode_command(cmd)

    @pyqtSlot()
    def on_x_dec_button_clicked(self):
        self.move_axis('X', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def on_x_add_button_clicked(self):
        self.move_axis('X', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def on_y_dec_button_clicked(self):
        self.move_axis('Y', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def on_y_add_button_clicked(self):
        self.move_axis('Y', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def on_z_dec_button_clicked(self):
        self.move_axis('Z', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def on_z_add_button_clicked(self):
        self.move_axis('Z', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot(QAbstractButton)
    def on_button_group_clicked(self, button):
        if button.text() == self.tr("Left"):
            self._printer.write_gcode_command('T0')
        elif button.text() == self.tr("Right"):
            self._printer.write_gcode_command('T1')
        elif button.text() in self.distance_list:
            if self.button_group.id(button) != self.distance_current_id:
                self.button_group.button(self.distance_current_id).setStyleSheet(uncheckedStyleSheet)
                self.button_group.button(self.button_group.id(button)).setStyleSheet(checkedStyleSheet)
                self.distance_current_id = self.button_group.id(button)

    def on_disabled_button_clicked(self):
        self._printer.write_gcode_command('M84')

    def on_update_printer_information(self):
        # switch button
        if self._printer.get_extruder() == "left":
            self.x_left_button.setStyleSheet(checkedStyleSheet)
            self.x_right_button.setStyleSheet(uncheckedStyleSheet)
        elif self._printer.get_extruder() == "right":
            self.x_left_button.setStyleSheet(uncheckedStyleSheet)
            self.x_right_button.setStyleSheet(checkedStyleSheet)

        self.x_frame_title.setText('X: {}'.format(self._printer.get_position('X')))
        self.y_frame_title.setText('Y: {}'.format(self._printer.get_position('Y')))
        self.z_frame_title.setText('Z: {}'.format(self._printer.get_position('Z')))
