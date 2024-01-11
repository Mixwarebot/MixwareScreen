from qtCore import *
from ui.base.baseLine import BaseHLine
from ui.base.basePushButton import BasePushButton
from ui.base.baseRound import BaseRoundDialog


class BabyStepPad(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.resize(self._width - 40, self._height / 2)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("babyStepFrame")
        self.frame.setStyleSheet("QFrame#babyStepFrame { border-radius: 10px; background: #FFFFFF; }")

        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setObjectName("title")
        self.title_frame.setFixedHeight(40)

        self.title_frame_layout = QHBoxLayout(self.title_frame)
        self.title_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.title_frame_layout.setSpacing(0)

        self.title_label = QLabel()
        self.title_label.setFixedHeight(40)
        self.title_frame_layout.addWidget(self.title_label)

        self.title_close_button = BasePushButton()
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.setFlat(True)
        self.title_close_button.clicked.connect(self.close_button_on_clicked)
        self.title_frame_layout.addWidget(self.title_close_button)
        self.frame_layout.addWidget(self.title_frame)

        self.tips_label = QLabel()
        self.tips_label.setObjectName("numberPadInformationLabel")
        self.tips_label.setAlignment(Qt.AlignCenter)
        self.tips_label.setFixedSize(self.width(), 90)
        self.tips_label.setWordWrap(True)
        self.frame_layout.addWidget(self.tips_label)

        self.distance_layout = QVBoxLayout()
        self.distance_layout.setContentsMargins(20, 0, 20, 0)
        self.distance_layout.setSpacing(0)

        self.baby_step_distance_title = QLabel()
        self.baby_step_distance_title.setObjectName("frame_title")
        self.baby_step_distance_title.setFixedHeight(40)
        self.distance_layout.addWidget(self.baby_step_distance_title)

        self.baby_step_distance_frame = QFrame()
        self.baby_step_distance_frame.setObjectName("frameBox")
        self.baby_step_distance_frame.setFixedHeight(88)

        self.distance_frame_layout = QHBoxLayout(self.baby_step_distance_frame)
        self.distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.distance_frame_layout.setSpacing(0)

        self.baby_step_button_group = QButtonGroup()
        self.baby_step_button_group.buttonClicked.connect(self.on_button_clicked)

        self.baby_step_distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self.baby_step_distance_default = "0.1"
        self.baby_step_distance_current_id = 0
        for d in range(len(self.baby_step_distance_list)):
            button = BasePushButton()
            button.setText(self.baby_step_distance_list[d])
            button.setObjectName("dataButton")
            self.baby_step_button_group.addButton(button, d)
            if self.baby_step_distance_list[d] == self.baby_step_distance_default:
                self.on_button_clicked(self.baby_step_button_group.button(d))
            self.distance_frame_layout.addWidget(button)
        self.distance_layout.addWidget(self.baby_step_distance_frame)
        self.frame_layout.addLayout(self.distance_layout)

        self.z_frame_layout = QVBoxLayout()
        self.z_frame_layout.setContentsMargins(20, 10, 20, 20)
        self.z_frame_layout.setSpacing(0)

        self.baby_step_offset_label = QLabel()
        self.baby_step_offset_label.setObjectName("frame_title")
        self.baby_step_offset_label.setFixedHeight(40)
        self.z_frame_layout.addWidget(self.baby_step_offset_label)

        self.baby_step_button_frame = QFrame()
        self.baby_step_button_frame.setObjectName("frameBox")

        self.z_button_frame_layout = QVBoxLayout(self.baby_step_button_frame)
        self.z_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.z_button_frame_layout.setSpacing(0)

        self.baby_step_button_lift = BasePushButton()
        self.baby_step_button_lift.setObjectName("upLogo")
        self.baby_step_button_lift.clicked.connect(self.on_baby_step_button_lift_clicked)
        self.z_button_frame_layout.addWidget(self.baby_step_button_lift)

        self.z_button_frame_layout.addWidget(BaseHLine())

        self.baby_step_button_drop = BasePushButton()
        self.baby_step_button_drop.setObjectName("downLogo")
        self.baby_step_button_drop.clicked.connect(self.on_baby_step_button_drop_clicked)
        self.z_button_frame_layout.addWidget(self.baby_step_button_drop)
        self.z_frame_layout.addWidget(self.baby_step_button_frame)
        self.frame_layout.addLayout(self.z_frame_layout)
        self.layout.addWidget(self.frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        if self._printer.get_extruder() == "right":
            self.title_label.setText(self.tr("Baby Step (Right)"))
        else:
            self.title_label.setText(self.tr("Baby Step (Left)"))
        self.title_close_button.setText("x")
        self.tips_label.setText(self.tr("(Tips: Baby Step will be delayed.)"))
        self.baby_step_distance_title.setText(self.tr("Move Distance (mm)"))
        self.baby_step_offset_label.setText("Z: 0")
        self.baby_step_button_lift.setTitle(self.tr("Lift Bed"))
        self.baby_step_button_drop.setTitle(self.tr("Drop Bed"))

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.baby_step_offset_label.setText(
            "Z: {}".format(self._printer.information['probe']['offset'][self._printer.get_extruder()]['Z']))

    @pyqtSlot(QAbstractButton)
    def on_button_clicked(self, button):
        if button.text() in self.baby_step_distance_list:
            if self.baby_step_button_group.id(button) != self.baby_step_distance_current_id:
                update_style(self.baby_step_button_group.button(self.baby_step_distance_current_id), "unchecked")
                update_style(self.baby_step_button_group.button(self.baby_step_button_group.id(button)), "checked")
                self.baby_step_distance_current_id = self.baby_step_button_group.id(button)

    @pyqtSlot()
    def on_baby_step_button_lift_clicked(self):
        self._printer.baby_step_lift(float(self.baby_step_distance_list[self.baby_step_distance_current_id]))

    @pyqtSlot()
    def on_baby_step_button_drop_clicked(self):
        self._printer.baby_step_drop(float(self.baby_step_distance_list[self.baby_step_distance_current_id]))

    def close_button_on_clicked(self):
        self.reject()
