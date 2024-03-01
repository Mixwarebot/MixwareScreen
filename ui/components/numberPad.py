from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.components.base.baseRound import BaseRoundDialog


class NumberPad(BaseRoundDialog):

    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()
        self.number = "0"
        self.numberObject = ""
        self._source = ""

        self.resize(self._width - 40, self._height / 2)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; background: #F2F2F2; }")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setAlignment(Qt.AlignTop)

        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")
        title_frame_layout = QHBoxLayout(self.title_frame)
        title_frame_layout.setContentsMargins(0, 0, 0, 0)
        title_frame_layout.setSpacing(0)
        self.title_label = QLabel()
        self.title_label.setFixedHeight(40)
        title_frame_layout.addWidget(self.title_label)
        self.title_close_button = BasePushButton()
        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.clicked.connect(self.on_close_button_clicked)
        title_frame_layout.addWidget(self.title_close_button)
        self.frame_layout.addWidget(self.title_frame)
        self.informationLabel = QLabel()
        self.informationLabel.setObjectName("numberPadInformationLabel")
        self.informationLabel.setFixedSize(self.width(), 90)
        self.informationLabel.setWordWrap(True)
        self.frame_layout.addWidget(self.informationLabel)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(10, 0, 10, 0)
        self.inputLabel = QLabel()
        self.inputLabel.setObjectName("numberPadInputLabel")
        self.inputLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.input_layout.addWidget(self.inputLabel, 3)
        self.deleteButton = BasePushButton()
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setFixedSize(100, 60)
        self.deleteButton.clicked.connect(self.on_delete_button_clicked)
        self.input_layout.addWidget(self.deleteButton, 1)
        self.frame_layout.addLayout(self.input_layout)

        self.keyboard_layout = QGridLayout()
        self.keyboard_layout.setContentsMargins(10, 10, 10, 10)
        self.keyboard_layout.setSpacing(10)
        self.button7 = BasePushButton()
        self.button7.clicked.connect(self.on_button7_clicked)
        self.keyboard_layout.addWidget(self.button7, 0, 0)
        self.button8 = BasePushButton()
        self.button8.clicked.connect(self.on_button8_clicked)
        self.keyboard_layout.addWidget(self.button8, 0, 1)
        self.button9 = BasePushButton()
        self.button9.clicked.connect(self.on_button9_clicked)
        self.keyboard_layout.addWidget(self.button9, 0, 2)
        self.button4 = BasePushButton()
        self.button4.clicked.connect(self.on_button4_clicked)
        self.keyboard_layout.addWidget(self.button4, 1, 0)
        self.button5 = BasePushButton()
        self.button5.clicked.connect(self.on_button5_clicked)
        self.keyboard_layout.addWidget(self.button5, 1, 1)
        self.button6 = BasePushButton()
        self.button6.clicked.connect(self.on_button6_clicked)
        self.keyboard_layout.addWidget(self.button6, 1, 2)
        self.button1 = BasePushButton()
        self.button1.clicked.connect(self.on_button1_clicked)
        self.keyboard_layout.addWidget(self.button1, 2, 0)
        self.button2 = BasePushButton()
        self.button2.clicked.connect(self.on_button2_clicked)
        self.keyboard_layout.addWidget(self.button2, 2, 1)
        self.button3 = BasePushButton()
        self.button3.clicked.connect(self.on_button3_clicked)
        self.keyboard_layout.addWidget(self.button3, 2, 2)
        self.button0 = BasePushButton()
        self.button0.clicked.connect(self.on_button0_clicked)
        self.keyboard_layout.addWidget(self.button0, 3, 0)
        self.dotButton = BasePushButton()
        self.dotButton.clicked.connect(self.on_dot_button_clicked)
        self.keyboard_layout.addWidget(self.dotButton, 3, 1)
        self.enterButton = BasePushButton()
        self.enterButton.clicked.connect(self.on_enterButton_clicked)
        self.keyboard_layout.addWidget(self.enterButton, 3, 2)
        self.frame_layout.addLayout(self.keyboard_layout)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.frame)

    def re_translate_ui(self):
        self.title_label.setText(self.tr("Parameter Setting"))
        self.informationLabel.setText(self.tr("Parameter Information."))
        self.deleteButton.setText(self.tr("Delete"))
        self.enterButton.setText(self.tr("Enter"))
        self.inputLabel.setText(self.number)
        self.button0.setText("0")
        self.button1.setText("1")
        self.button2.setText("2")
        self.button3.setText("3")
        self.button4.setText("4")
        self.button5.setText("5")
        self.button6.setText("6")
        self.button7.setText("7")
        self.button8.setText("8")
        self.button9.setText("9")
        self.dotButton.setText(".")

    def add_number(self, n: str):
        if len(self.number) == 1 and self.number == "0" and n != ".":
            self.number = ""
        if len(self.number) > 2 and n != ".":
            if "." not in self.number and len(self.number) < 5:
                self.number += n
            elif "." in self.number and len(self.number) < 8 and self.number[-3] != ".":
                self.number += n
        else:
            self.number += n
        self.inputLabel.setText(self.number)

    def on_button0_clicked(self):
        self.add_number("0")

    def on_button1_clicked(self):
        self.add_number("1")

    def on_button2_clicked(self):
        self.add_number("2")

    def on_button3_clicked(self):
        self.add_number("3")

    def on_button4_clicked(self):
        self.add_number("4")

    def on_button5_clicked(self):
        self.add_number("5")

    def on_button6_clicked(self):
        self.add_number("6")

    def on_button7_clicked(self):
        self.add_number("7")

    def on_button8_clicked(self):
        self.add_number("8")

    def on_button9_clicked(self):
        self.add_number("9")

    def on_dot_button_clicked(self):
        if "." not in self.number:
            self.add_number(".")

    def on_delete_button_clicked(self):
        if len(self.number) > 1:
            self.number = self.number[:-1]
        else:
            self.number = "0"
        self.inputLabel.setText(self.number)

    def on_close_button_clicked(self):
        if self._source in ["dial_indicator_left", "dial_indicator_right"]:
            return
        self.reject()

    def on_enterButton_clicked(self):
        if "thermal_left" in self._source:
            value = 350 if int(self.number) > 350 else int(self.number)
            self._printer.set_thermal("left", value)
        elif "thermal_right" in self._source:
            value = 350 if int(self.number) > 350 else int(self.number)
            self._printer.set_thermal("right", value)
        elif "thermal_bed" in self._source:
            value = 120 if int(self.number) > 120 else int(self.number)
            self._printer.set_thermal("bed", value)
        elif "thermal_chamber" in self._source:
            value = 60 if int(self.number) > 60 else int(self.number)
            self._printer.set_thermal("chamber", value)
        elif "fan_left" in self._source:
            value = 100 if int(self.number) > 100 else int(self.number)
            self._printer.set_fan_speed("left", value / 100.0)
        elif "fan_right" in self._source:
            value = 100 if int(self.number) > 100 else int(self.number)
            self._printer.set_fan_speed("right", value / 100.0)
        elif "fan_exhaust" in self._source:
            value = 100 if int(self.number) > 100 else int(self.number)
            self._printer.set_fan_speed("exhaust", value / 100.0)
        elif "print_feed_rate" in self._source:
            value = 500 if int(self.number) > 500 else int(self.number)
            self._printer.write_gcode_command(f"M220 S{value}\nM220")
        elif "print_flow" in self._source:
            value = 500 if int(self.number) > 500 else int(self.number)
            extruder = 0 if self._printer.get_extruder() == 'left' else 1
            self._printer.write_gcode_command(f"M221 T{extruder} S{value}\nM221 T{extruder}")
        elif "step_x" in self._source:
            self._printer.write_gcode_command(f"fM92 X{self.number}\nM500\nM92")
        elif "step_y" in self._source:
            self._printer.write_gcode_command(f"M92 Y{self.number}\nM500\nM92")
        elif "step_z" in self._source:
            self._printer.write_gcode_command(f"M92 Z{self.number}\nM500\nM92")
        elif "step_e" in self._source:
            self._printer.write_gcode_command(f"M92 E{self.number}\nM500\nM92")
        elif "feed_rate_x" in self._source:
            self._printer.write_gcode_command(f"M203 X{self.number}\nM500\nM203")
        elif "feed_rate_y" in self._source:
            self._printer.write_gcode_command(f"M203 Y{self.number}\nM500\nM203")
        elif "feed_rate_z" in self._source:
            self._printer.write_gcode_command(f"M203 Z{self.number}\nM500\nM203")
        elif "feed_rate_e" in self._source:
            self._printer.write_gcode_command(f"M203 E{self.number}\nM500\nM203")
        elif "acceleration_x" in self._source:
            self._printer.write_gcode_command(f"M201 X{self.number}\nM500\nM201")
        elif "acceleration_y" in self._source:
            self._printer.write_gcode_command(f"M201 Y{self.number}\nM500\nM201")
        elif "acceleration_z" in self._source:
            self._printer.write_gcode_command(f"M201 Z{self.number}\nM500\nM201")
        elif "acceleration_e" in self._source:
            self._printer.write_gcode_command(f"M201 E{self.number}\nM500\nM201")
        elif "acceleration_print" in self._source:
            self._printer.write_gcode_command(f"M204 P{self.number}\nM500\nM204")
        elif "acceleration_retract" in self._source:
            self._printer.write_gcode_command(f"M204 R{self.number}\nM500\nM204")
        elif "acceleration_travel" in self._source:
            self._printer.write_gcode_command(f"M204 T{self.number}\nM500\nM204")
        elif "jerk_x" in self._source:
            self._printer.write_gcode_command(f"M205 X{self.number}\nM500\nM205")
        elif "jerk_y" in self._source:
            self._printer.write_gcode_command(f"M205 Y{self.number}\nM500\nM205")
        elif "jerk_z" in self._source:
            self._printer.write_gcode_command(f"M205 Z{self.number}\nM500\nM205")
        elif "jerk_e" in self._source:
            self._printer.write_gcode_command(f"M205 E{self.number}\nM500\nM205")
        elif "current_x" in self._source:
            self._printer.write_gcode_command(f"M906 X{self.number}\nM500\nM906")
        elif "current_x2" in self._source:
            self._printer.write_gcode_command(f"M906 I1 X{self.number}\nM500\nM906")
        elif "current_y" in self._source:
            self._printer.write_gcode_command(f"M906 Y{self.number}\nM500\nM906")
        elif "current_z" in self._source:
            self._printer.write_gcode_command(f"M906 Z{self.number}\nM500\nM906")
        elif "current_z2" in self._source:
            self._printer.write_gcode_command(f"M906 I1 Z{self.number}\nM500\nM906")
        elif "current_e" in self._source:
            self._printer.write_gcode_command(f"M906 T0 E{self.number}\nM500\nM906")
        elif "current_e2" in self._source:
            self._printer.write_gcode_command(f"M906 T1 E{self.number}\nM500\nM906")
        elif "frequency_x" in self._source:
            self._printer.write_gcode_command(f"M593 X F{self.number}\nM500\nM593")
        elif "frequency_y" in self._source:
            self._printer.write_gcode_command(f"M593 Y F{self.number}\nM500\nM593")
        elif "damping_x" in self._source:
            self._printer.write_gcode_command(f"M593 X D{self.number}\nM500\nM593")
        elif "damping_y" in self._source:
            self._printer.write_gcode_command(f"M593 Y D{self.number}\nM500\nM593")
        elif "linear_advance" in self._source:
            self._printer.write_gcode_command(f"M900 K{self.number}\nM500\nM900")
        elif "dial_indicator_left" in self._source:
            if self.number != "0":
                self._printer.set_dial_indicator_value("left", self.number)
            else:
                return
        elif "dial_indicator_right" in self._source:
            if self.number != "0":
                self._printer.set_dial_indicator_value("right", self.number)
            else:
                return
        self.close()

    def start(self, message: str, source: str):
        self.re_translate_ui()
        self.number = "0"
        self.inputLabel.setText(self.number)

        self._source = source
        if source == "thermal_left":
            message = self.tr("Extruder Left Target Temperature: {}°C").format(
                int(self._printer.information['thermal']['left']['target']))
        elif source == "thermal_right":
            message = self.tr("Extruder Right Target Temperature: {}°C").format(
                int(self._printer.information['thermal']['right']['target']))
        elif source == "thermal_bed":
            message = self.tr("Hot Bed Target Temperature: {}°C").format(
                int(self._printer.information['thermal']['bed']['target']))
        elif source == "thermal_chamber":
            message = self.tr("Chamber Target Temperature: {}°C").format(
                int(self._printer.information['thermal']['chamber']['target']))
        self.informationLabel.setText(message)

        self.exec()
