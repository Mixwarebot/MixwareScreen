from qtCore import *
from ui.base.baseLine import BaseHLine
from ui.base.basePushButton import BasePushButton
from ui.base.baseRound import BaseRoundDialog


class BabyStepPad(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.frame = QFrame()

        self.title_frame = QFrame()
        self.title_label = QLabel()
        self.title_close_button = BasePushButton()

        self.tips_label = QLabel()

        self.baby_step_distance_title = QLabel()
        self.baby_step_distance_frame = QFrame()
        self.baby_step_distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self.baby_step_distance_default = "0.1"
        self.baby_step_distance_current_id = 0

        self.baby_step_offset_label = QLabel()
        self.baby_step_button_frame = QFrame()
        self.baby_step_button_group = QButtonGroup()
        self.baby_step_button_up = BasePushButton()
        self.baby_step_button_down = BasePushButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.setWindowTitle("NumberPad")
        self.resize(self._width-40, self._height/2)
        self.move((self._width - self.width())/2, (self._height - self.height())/2)

        self.frame.setObjectName("babyStepFrame")
        self.frame.setStyleSheet("QFrame#babyStepFrame { border-radius: 10px; background: #FFFFFF; }")

        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")
        self.title_label.setFixedHeight(40)
        self.title_label.setText(self.tr("Baby Step({})".format(self.tr(self._printer.get_extruder().title()))))
        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)

        self.tips_label.setObjectName("numberPadInformationLabel")
        self.tips_label.setAlignment(Qt.AlignCenter)
        self.tips_label.setFixedSize(self.width(), 90)
        self.tips_label.setText(self.tr("(Tips: Baby Step will be delayed.)"))
        self.tips_label.setWordWrap(True)

        self.baby_step_distance_frame.setObjectName("frameBox")
        self.baby_step_distance_frame.setFixedHeight(88)
        self.baby_step_distance_title.setText(self.tr("Move Distance (mm)"))
        self.baby_step_distance_title.setFixedHeight(40)
        self.baby_step_distance_title.setObjectName("frame_title")
        self.baby_step_button_frame.setObjectName("frameBox")
        self.baby_step_button_up.setObjectName("upLogo")
        self.baby_step_button_down.setObjectName("downLogo")
        self.baby_step_offset_label.setText("Z: 0")
        self.baby_step_offset_label.setFixedHeight(40)
        self.baby_step_offset_label.setObjectName("frame_title")

    def initLayout(self):
        title_frame_layout = QHBoxLayout(self.title_frame)
        title_frame_layout.setContentsMargins(0, 0, 0, 0)
        title_frame_layout.setSpacing(0)
        title_frame_layout.addWidget(self.title_label)
        title_frame_layout.addWidget(self.title_close_button)

        distance_frame_layout = QHBoxLayout(self.baby_step_distance_frame)
        distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        distance_frame_layout.setSpacing(0)
        for d in range(len(self.baby_step_distance_list)):
            button = BasePushButton()
            button.setText(self.baby_step_distance_list[d])
            button.setObjectName("dataButton")
            self.baby_step_button_group.addButton(button, d)
            if self.baby_step_distance_list[d] == self.baby_step_distance_default:
                self.on_button_clicked(self.baby_step_button_group.button(d))
            distance_frame_layout.addWidget(button)

        distance_layout = QVBoxLayout()
        distance_layout.setContentsMargins(20, 0, 20, 0)
        distance_layout.setSpacing(0)
        distance_layout.addWidget(self.baby_step_distance_title)
        distance_layout.addWidget(self.baby_step_distance_frame)

        z_button_frame_layout = QVBoxLayout(self.baby_step_button_frame)
        z_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        z_button_frame_layout.setSpacing(0)
        z_button_frame_layout.addWidget(self.baby_step_button_up)
        z_button_frame_layout.addWidget(BaseHLine())
        z_button_frame_layout.addWidget(self.baby_step_button_down)

        z_frame_layout = QVBoxLayout()
        z_frame_layout.setContentsMargins(20, 10, 20, 20)
        z_frame_layout.setSpacing(0)
        z_frame_layout.addWidget(self.baby_step_offset_label)
        z_frame_layout.addWidget(self.baby_step_button_frame)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_frame)
        layout.addWidget(self.tips_label)
        layout.addLayout(distance_layout)
        layout.addLayout(z_frame_layout)
        # layout.setAlignment(Qt.AlignTop)

        _layout = QVBoxLayout(self)
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)
        _layout.addWidget(self.frame)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self.title_close_button.clicked.connect(self.close_button_on_clicked)
        self.baby_step_button_group.buttonClicked.connect(self.on_button_clicked)
        self.baby_step_button_up.clicked.connect(self.on_z_button_1_clicked)
        self.baby_step_button_down.clicked.connect(self.on_z_button_2_clicked)

    @pyqtSlot(QAbstractButton)
    def on_button_clicked(self, button):
        if button.text() in self.baby_step_distance_list:
            if self.baby_step_button_group.id(button) != self.baby_step_distance_current_id:
                self.baby_step_button_group.button(self.baby_step_distance_current_id).setStyleSheet(uncheckedStyleSheet)
                self.baby_step_button_group.button(self.baby_step_button_group.id(button)).setStyleSheet(checkedStyleSheet)
                self.baby_step_distance_current_id = self.baby_step_button_group.id(button)

    @pyqtSlot()
    def on_z_button_1_clicked(self):
        self._printer.write_gcode_command(f'M290 Z-{self.baby_step_distance_list[self.baby_step_distance_current_id]}\nM851\nM218')

    @pyqtSlot()
    def on_z_button_2_clicked(self):
        self._printer.write_gcode_command(f'M290 Z{self.baby_step_distance_list[self.baby_step_distance_current_id]}\nM851\nM218')

    def close_button_on_clicked(self):
        self.reject()

    @pyqtSlot()
    def on_update_printer_information(self):
        self.baby_step_offset_label.setText("Z: {}".format(self._printer.information['probe']['offset'][self._printer.get_extruder()]['Z']))