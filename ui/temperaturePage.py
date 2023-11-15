from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.printerPage import TemperatureBox


class TemperaturePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent
        self.heater = 'left'

        self.setObjectName("temperaturePage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.temperature_box = TemperatureBox(self._printer)
        self.temperature_group = QButtonGroup()
        self.temperature_group.idClicked.connect(self.on_temperature_button_group_clicked)
        self.temperature_group.addButton(self.temperature_box.left, 0)
        self.temperature_group.addButton(self.temperature_box.right, 1)
        self.temperature_group.addButton(self.temperature_box.bed, 2)
        self.temperature_group.addButton(self.temperature_box.chamber, 3)
        self.layout.addWidget(self.temperature_box, 5)

        degree_layout = QVBoxLayout()
        degree_layout.setContentsMargins(0, 0, 0, 0)
        degree_layout.setSpacing(0)

        self.degree_title = QLabel()
        self.degree_title.setText(self.tr("Heating Degeee"))
        self.degree_title.setFixedHeight(40)
        self.degree_title.setStyleSheet("padding-left: 10px;")
        degree_layout.addWidget(self.degree_title)

        self.degree_frame = QFrame()
        self.degree_frame.setObjectName("frameBox")
        self.degree_frame.setFixedHeight(88)
        self.degree_list = ["1", "5", "10", "20"]
        self.degree_default = "10"
        self.degree_current_id = 0

        degree_frame_layout = QHBoxLayout(self.degree_frame)
        degree_frame_layout.setContentsMargins(5, 1, 5, 1)
        degree_frame_layout.setSpacing(0)

        self.degree_group = QButtonGroup()
        self.degree_group.buttonClicked.connect(self.on_degree_button_group_clicked)
        for d in range(len(self.degree_list)):
            button = BasePushButton()
            button.setText(self.degree_list[d])
            button.setObjectName("dataButton")
            self.degree_group.addButton(button, d)
            if self.degree_list[d] == self.degree_default:
                self.on_degree_button_group_clicked(self.degree_group.button(d))
            degree_frame_layout.addWidget(button)
        degree_layout.addWidget(self.degree_frame)
        self.layout.addLayout(degree_layout)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("BasePushButton {border: 1px solid #D4D4D4;}")
        button_layout = QHBoxLayout(self.frame)

        button_left_layout = QVBoxLayout()
        self.pla_button = BasePushButton()
        self.pla_button.clicked.connect(self.on_pla_button_clicked)
        button_left_layout.addWidget(self.pla_button)
        self.pa_cf_button = BasePushButton()
        self.pa_cf_button.clicked.connect(self.on_pa_cf_button_clicked)
        button_left_layout.addWidget(self.pa_cf_button)
        self.cool_button = BasePushButton()
        self.cool_button.clicked.connect(self.on_cool_button_clicked)
        button_left_layout.addWidget(self.cool_button)
        button_layout.addLayout(button_left_layout, 1)
        button_right_layout = QVBoxLayout()
        self.add_button = BasePushButton()
        self.add_button.setText("+")
        self.add_button.clicked.connect(self.on_add_button_clicked)
        button_right_layout.addWidget(self.add_button)
        self.dec_button = BasePushButton()
        self.dec_button.setText("-")
        self.dec_button.clicked.connect(self.on_dec_button_clicked)
        button_right_layout.addWidget(self.dec_button)
        button_layout.addLayout(button_right_layout, 1)
        self.layout.addWidget(self.frame, 4)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.pla_button.setText(self.tr("PLA"))
        self.pa_cf_button.setText(self.tr("PA-CF"))
        self.cool_button.setText(self.tr("Cool"))

    def change_target_temperature(self, heater: str, degree: int):
        if heater in ['left', 'right', 'bed', 'chamber']:
            degree += int(self._printer.information['thermal'][heater]['target'])
            if degree < 0: degree = 0
            if degree > 350: degree = 350
            if heater == 'bed' and degree > 110: degree = 110
            if heater == 'chamber' and degree > 60: degree = 60
            self._printer.set_thermal(heater, degree)

    @pyqtSlot(QAbstractButton)
    def on_degree_button_group_clicked(self, button):
        if button.text() in self.degree_list:
            if self.degree_group.id(button) != self.degree_current_id:
                self.degree_group.button(self.degree_current_id).setStyleSheet(uncheckedStyleSheet)
                self.degree_group.button(self.degree_group.id(button)).setStyleSheet(checkedStyleSheet)
                self.degree_current_id = self.degree_group.id(button)

    @pyqtSlot()
    def on_temperature_button_group_clicked(self, id):
        thermal = ['left', 'right', 'bed', 'chamber']
        if 0 <= id <= 3:
            self.heater = thermal[id]
            for i in range(4):
                if i == id: self.temperature_group.button(i).setStyleSheet(checkedStyleSheet)
                else: self.temperature_group.button(i).setStyleSheet(uncheckedStyleSheet)

    @pyqtSlot()
    def on_add_button_clicked(self):
        self.change_target_temperature(self.heater, int(self.degree_list[self.degree_current_id]))

    @pyqtSlot()
    def on_dec_button_clicked(self):
        self.change_target_temperature(self.heater, -int(self.degree_list[self.degree_current_id]))

    @pyqtSlot()
    def on_cool_button_clicked(self):
        self._printer.set_thermal('left', 0)
        self._printer.set_thermal('right', 0)
        self._printer.set_thermal('bed', 0)
        # self._printer.set_temperatures('chamber', 0)

    @pyqtSlot()
    def on_pla_button_clicked(self):
        self._printer.set_thermal('left', 210)
        self._printer.set_thermal('right', 210)
        self._printer.set_thermal('bed', 60)
        # self._printer.set_temperatures('chamber', 35)

    @pyqtSlot()
    def on_pa_cf_button_clicked(self):
        self._printer.set_thermal('left', 300)
        self._printer.set_thermal('right', 300)
        self._printer.set_thermal('bed', 90)
        # self._printer.set_temperatures('chamber', 50)