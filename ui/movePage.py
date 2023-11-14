from qtCore import *
from ui.base.baseLine import BaseVLine, BaseHLine
from ui.base.basePushButton import BasePushButton


class MovePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("movePage")

        self._layout = QVBoxLayout(self)

        self.buttonGroup = QButtonGroup()

        self.frame = QFrame()

        self.x_left_button = BasePushButton()
        self.x_right_button = BasePushButton()
        self.x_frame_title = QLabel()
        self.x_button_frame = QFrame()
        self.x_button_1 = BasePushButton()
        self.x_button_2 = BasePushButton()

        self.y_frame_title = QLabel()
        self.y_button_frame = QFrame()
        self.y_button_1 = BasePushButton()
        self.y_button_2 = BasePushButton()

        self.z_frame_title = QLabel()
        self.z_button_frame = QFrame()
        self.z_button_1 = BasePushButton()
        self.z_button_2 = BasePushButton()

        self.speed = QLabel()
        self.speed_frame = QFrame()
        self.speed_title = QLabel()
        self.speed_slider = QSlider()

        self.disabled_button = BasePushButton()

        self.distance_title = QLabel()
        self.distance_frame = QFrame()
        self.distance_list = ["0.1", "0.5", "1", "5", "10", "50", "100"]
        self.distance_default = "10"
        self.distance_current_id = 0

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self._layout.setContentsMargins(20, 0, 20, 0)
        self._layout.setSpacing(0)

        self.frame.setObjectName("frameBox")
        self.x_button_frame.setObjectName("frameBox")
        self.y_button_frame.setObjectName("frameBox")
        self.z_button_frame.setObjectName("frameBox")
        self.speed_frame.setObjectName("frameBox")
        self.distance_frame.setObjectName("frameBox")
        self.distance_frame.setFixedHeight(88)

        self.x_left_button.setObjectName("extruderButton")
        self.x_left_button.setFixedHeight(64)
        self.x_left_button.setText(self.tr("Left"))
        self.x_right_button.setObjectName("extruderButton")
        self.x_right_button.setFixedHeight(64)
        self.x_right_button.setText(self.tr("Right"))
        self.buttonGroup.addButton(self.x_left_button)
        self.buttonGroup.addButton(self.x_right_button)

        self.x_button_1.setObjectName("leftLogo")
        self.x_button_2.setObjectName("rightLogo")
        self.y_button_1.setObjectName("upLogo")
        self.y_button_2.setObjectName("downLogo")
        self.z_button_1.setObjectName("upLogo")
        self.z_button_2.setObjectName("downLogo")

        self.x_frame_title.setText("X: 0")
        self.x_frame_title.setFixedHeight(40)
        self.x_frame_title.setObjectName("frame_title")
        self.y_frame_title.setText("Y: 0")
        self.y_frame_title.setFixedHeight(40)
        self.y_frame_title.setObjectName("frame_title")
        self.z_frame_title.setText("Z: 0")
        self.z_frame_title.setFixedHeight(40)
        self.z_frame_title.setObjectName("frame_title")

        self.speed_title.setText(self.tr("Speed"))
        self.speed_title.setFixedHeight(40)
        self.speed_title.setAlignment(Qt.AlignCenter)
        self.speed_title.setStyleSheet("background: transparent; padding: 0;")
        self.distance_title.setText(self.tr("Move Distance (mm)"))
        self.distance_title.setFixedHeight(40)
        self.distance_title.setObjectName("frame_title")

        self.speed.setText("100%")
        self.speed.setFixedHeight(40)
        self.speed.setAlignment(Qt.AlignCenter)

        self.disabled_button.setText(self.tr("Unlock\nMotor"))
        self.disabled_button.setMaximumHeight(128)
        self.disabled_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.disabled_button.setStyleSheet("border: 1px solid #D4D4D4; border-radius: 10px")

        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(100)
        self.speed_slider.setStyleSheet("QSlider::groove {border: none; border-radius: 10px; background-color: #E4E4E4;}"
                                        "QSlider::groove:vertical {width: 20px;} "
                                        "QSlider::handle {background-color: #FFFFFF; width: 36px; height: 36px; border: 1px solid #C8C8C8; border-radius: 18px; margin: 0;}"
                                        "QSlider::handle:vertical {margin-left: -9px; margin-right: -9px;}"
                                        "QSlider::sub-page, QSlider::add-page{border: none; border-radius: 10px;}")
        self.speed_slider.setTickPosition(QSlider.TicksRight)
        self.speed_slider.setTickInterval(20)
        self.speed_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.onButtonClicked(self.x_left_button)

    def initLayout(self):
        x_button_frame_top_layout = QHBoxLayout()
        x_button_frame_top_layout.addWidget(self.x_left_button)
        x_button_frame_top_layout.addWidget(self.x_right_button)

        x_button_frame_bottom_layout = QHBoxLayout()
        x_button_frame_bottom_layout.addWidget(self.x_button_1)
        x_button_frame_bottom_layout.addWidget(BaseVLine())
        x_button_frame_bottom_layout.addWidget(self.x_button_2)

        x_button_frame_layout = QVBoxLayout(self.x_button_frame)
        x_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        x_button_frame_layout.setSpacing(0)
        x_button_frame_layout.addLayout(x_button_frame_top_layout)
        x_button_frame_layout.addWidget(BaseHLine())
        x_button_frame_layout.addLayout(x_button_frame_bottom_layout)

        x_frame_layout = QVBoxLayout()
        x_frame_layout.setSpacing(0)
        x_frame_layout.addWidget(self.x_frame_title)
        x_frame_layout.addWidget(self.x_button_frame)

        y_button_frame_layout = QVBoxLayout(self.y_button_frame)
        y_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        y_button_frame_layout.setSpacing(0)
        y_button_frame_layout.addWidget(self.y_button_1)
        y_button_frame_layout.addWidget(BaseHLine())
        y_button_frame_layout.addWidget(self.y_button_2)

        y_frame_layout = QVBoxLayout()
        y_frame_layout.setSpacing(0)
        y_frame_layout.addWidget(self.y_frame_title)
        y_frame_layout.addWidget(self.y_button_frame)

        z_button_frame_layout = QVBoxLayout(self.z_button_frame)
        z_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        z_button_frame_layout.setSpacing(0)
        z_button_frame_layout.addWidget(self.z_button_1)
        z_button_frame_layout.addWidget(BaseHLine())
        z_button_frame_layout.addWidget(self.z_button_2)

        z_frame_layout = QVBoxLayout()
        z_frame_layout.setSpacing(0)
        z_frame_layout.addWidget(self.z_frame_title)
        z_frame_layout.addWidget(self.z_button_frame)

        axis_frame_layout_2 = QHBoxLayout()
        axis_frame_layout_2.setSpacing(10)
        axis_frame_layout_2.addLayout(y_frame_layout)
        axis_frame_layout_2.addLayout(z_frame_layout)

        axis_frame_layout = QVBoxLayout()
        axis_frame_layout.setContentsMargins(0, 0, 0, 0)
        axis_frame_layout.setSpacing(20)
        axis_frame_layout.addLayout(x_frame_layout, 1)
        axis_frame_layout.addLayout(axis_frame_layout_2, 1)

        speed_frame_layout = QVBoxLayout(self.speed_frame)
        speed_frame_layout.setContentsMargins(0, 10, 0, 20)
        speed_frame_layout.setSpacing(10)
        speed_frame_layout.addWidget(self.speed)
        speed_frame_layout.addWidget(self.speed_slider)

        frame_middle_left_layout = QVBoxLayout()
        frame_middle_left_layout.setContentsMargins(0, 0, 0, 0)
        frame_middle_left_layout.setSpacing(0)
        frame_middle_left_layout.addWidget(self.speed_title)
        frame_middle_left_layout.addWidget(self.speed_frame)
        frame_middle_left_layout.addSpacing(20)
        frame_middle_left_layout.addWidget(self.disabled_button)

        frame_midle_layout = QHBoxLayout()
        frame_midle_layout.setContentsMargins(0, 0, 0, 0)
        frame_midle_layout.addLayout(frame_middle_left_layout, 1)
        frame_midle_layout.addLayout(axis_frame_layout, 3)

        distance_frame_layout = QHBoxLayout(self.distance_frame)
        distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        distance_frame_layout.setSpacing(0)
        for d in range(len(self.distance_list)):
            button = BasePushButton()
            button.setText(self.distance_list[d])
            button.setObjectName("dataButton")
            self.buttonGroup.addButton(button, d)
            if self.distance_list[d] == self.distance_default:
                self.onButtonClicked(self.buttonGroup.button(d))
            distance_frame_layout.addWidget(button)

        distance_layout = QVBoxLayout()
        distance_layout.setContentsMargins(0, 0, 0, 0)
        distance_layout.setSpacing(0)
        distance_layout.addWidget(self.distance_title)
        distance_layout.addWidget(self.distance_frame)

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(20)
        frame_layout.addLayout(distance_layout, 1)
        frame_layout.addLayout(frame_midle_layout, 5)

        self._layout.addWidget(self.frame)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.buttonGroup.buttonClicked.connect(self.onButtonClicked)
        self.speed_slider.valueChanged.connect(self.onSliderValueChanged)
        self.x_button_1.clicked.connect(self.onXDecButtonClicked)
        self.x_button_2.clicked.connect(self.onXAddButtonClicked)
        self.y_button_1.clicked.connect(self.onYAddButtonClicked)
        self.y_button_2.clicked.connect(self.onYDecButtonClicked)
        self.z_button_1.clicked.connect(self.onZDecButtonClicked)
        self.z_button_2.clicked.connect(self.onZAddButtonClicked)
        self.disabled_button.clicked.connect(self.onDisabledButtonClicked)

    @pyqtSlot()
    def onSliderValueChanged(self):
        self.speed.setText(str(self.speed_slider.value()) + '%')

    def moveAxis(self, axis: str, pos: float):
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
                elif pos > 320:
                    pos = 320
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
    def onXDecButtonClicked(self):
        self.moveAxis('X', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def onXAddButtonClicked(self):
        self.moveAxis('X', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def onYDecButtonClicked(self):
        self.moveAxis('Y', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def onYAddButtonClicked(self):
        self.moveAxis('Y', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def onZDecButtonClicked(self):
        self.moveAxis('Z', -float(self.distance_list[self.distance_current_id]))

    @pyqtSlot()
    def onZAddButtonClicked(self):
        self.moveAxis('Z', float(self.distance_list[self.distance_current_id]))

    @pyqtSlot(QAbstractButton)
    def onButtonClicked(self, button):
        if button.text() == self.tr("Left"):
            self._printer.write_gcode_command('T0')
        elif button.text() == self.tr("Right"):
            self._printer.write_gcode_command('T1')
        elif button.text() in self.distance_list:
            if self.buttonGroup.id(button) != self.distance_current_id:
                self.buttonGroup.button(self.distance_current_id).setStyleSheet(uncheckedStyleSheet)
                self.buttonGroup.button(self.buttonGroup.id(button)).setStyleSheet(checkedStyleSheet)
                self.distance_current_id = self.buttonGroup.id(button)

    def onDisabledButtonClicked(self):
        self._printer.write_gcode_command('M84')

    def onUpdatePrinterInformation(self):
        if self._printer.get_extruder() == "left":
            self.x_left_button.setStyleSheet(checkedStyleSheet)
            self.x_right_button.setStyleSheet(uncheckedStyleSheet)
        elif self._printer.get_extruder() == "right":
            self.x_left_button.setStyleSheet(uncheckedStyleSheet)
            self.x_right_button.setStyleSheet(checkedStyleSheet)

        self.x_frame_title.setText('X: {}'.format(self._printer.get_position('X')))
        self.y_frame_title.setText('Y: {}'.format(self._printer.get_position('Y')))
        self.z_frame_title.setText('Z: {}'.format(self._printer.get_position('Z')))
