from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.components.temperatureBox import TemperatureBox


class TemperaturePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent
        self.heater = {
            'left': False,
            'right': False,
            'bed': False,
            'chamber': False
        }
        self.thermal = list(self.heater.keys())

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

        self.degree_layout = QVBoxLayout()
        self.degree_layout.setContentsMargins(0, 0, 0, 0)
        self.degree_layout.setSpacing(0)

        self.degree_title = QLabel()
        self.degree_title.setFixedHeight(40)
        self.degree_title.setStyleSheet("padding-left: 10px;")
        self.degree_layout.addWidget(self.degree_title)

        self.degree_frame = QFrame()
        self.degree_frame.setObjectName("frameBox")
        self.degree_frame.setFixedHeight(88)
        self.degree_list = ["1", "5", "10", "20"]
        self.degree_default = "10"
        self.degree_current_id = 0

        self.degree_frame_layout = QHBoxLayout(self.degree_frame)
        self.degree_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.degree_frame_layout.setSpacing(0)

        self.degree_group = QButtonGroup()
        self.degree_group.buttonClicked.connect(self.on_degree_button_group_clicked)
        for d in range(len(self.degree_list)):
            button = BasePushButton()
            button.setText(self.degree_list[d])
            button.setObjectName("dataButton")
            self.degree_group.addButton(button, d)
            if self.degree_list[d] == self.degree_default:
                self.on_degree_button_group_clicked(self.degree_group.button(d))
            self.degree_frame_layout.addWidget(button)
        self.degree_layout.addWidget(self.degree_frame)
        self.layout.addLayout(self.degree_layout)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("BasePushButton {border: 1px solid #D4D4D4;}")
        self.button_layout = QHBoxLayout(self.frame)
        self.button_layout.setContentsMargins(20, 20, 20, 20)
        self.button_layout.setSpacing(20)

        self.button_left_layout = QVBoxLayout()
        self.button_left_layout.setContentsMargins(0, 0, 0, 0)
        self.button_left_layout.setSpacing(20)
        self.pla_button = BasePushButton()
        self.pla_button.clicked.connect(self.on_pla_button_clicked)
        self.button_left_layout.addWidget(self.pla_button)
        self.pa_cf_button = BasePushButton()
        self.pa_cf_button.clicked.connect(self.on_pa_cf_button_clicked)
        self.button_left_layout.addWidget(self.pa_cf_button)
        self.cool_button = BasePushButton()
        self.cool_button.clicked.connect(self.on_cool_button_clicked)
        self.button_left_layout.addWidget(self.cool_button)
        self.button_layout.addLayout(self.button_left_layout, 1)
        self.button_right_layout = QVBoxLayout()
        self.button_right_layout.setContentsMargins(0, 0, 0, 0)
        self.button_right_layout.setSpacing(20)
        self.add_button = BasePushButton()
        self.add_button.setText("+")
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.button_right_layout.addWidget(self.add_button)
        self.dec_button = BasePushButton()
        self.dec_button.setText("-")
        self.dec_button.clicked.connect(self.on_dec_button_clicked)
        self.button_right_layout.addWidget(self.dec_button)
        self.button_layout.addLayout(self.button_right_layout, 1)
        self.layout.addWidget(self.frame, 4)

        self.on_temperature_button_group_clicked(0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.pla_button.setText(self.tr("PLA"))
        self.pa_cf_button.setText(self.tr("PA-CF"))
        self.cool_button.setText(self.tr("Cool"))
        self.degree_title.setText(self.tr("Heating Degree"))

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
                update_style(self.degree_group.button(self.degree_current_id), "unchecked")
                update_style(self.degree_group.button(self.degree_group.id(button)), "checked")
                self.degree_current_id = self.degree_group.id(button)

    @pyqtSlot(int)
    def on_temperature_button_group_clicked(self, _id):
        self.heater[self.thermal[_id]] = not self.heater[self.thermal[_id]]
        update_style(self.temperature_group.button(_id), "checked" if self.heater[self.thermal[_id]] else "unchecked")

    def show_tips(self):
        have_heater = False
        for thermal in self.thermal:
            if self.heater[thermal]: have_heater = True
        if not have_heater:
            self._printer.updatePrinterMessage.emit(self.tr("Please select a heater."), 1)

    @pyqtSlot()
    def on_add_button_clicked(self):
        for thermal in self.thermal:
            if self.heater[thermal]:
                self.change_target_temperature(thermal, int(self.degree_list[self.degree_current_id]))
        self.show_tips()

    @pyqtSlot()
    def on_dec_button_clicked(self):
        for thermal in self.thermal:
            if self.heater[thermal]:
                self.change_target_temperature(thermal, -int(self.degree_list[self.degree_current_id]))
        self.show_tips()

    @pyqtSlot()
    def on_cool_button_clicked(self):
        for thermal in self.thermal:
            if self.heater[thermal]:
                self._printer.set_thermal(thermal, 0)
        self.show_tips()

    @pyqtSlot()
    def on_pla_button_clicked(self):
        if self.heater['left']:
            self._printer.set_thermal('left', 210)
        if self.heater['right']:
            self._printer.set_thermal('right', 210)
        if self.heater['bed']:
            self._printer.set_thermal('bed', 60)
        if self.heater['chamber']:
            self._printer.set_thermal('chamber', 35)
        self.show_tips()

    @pyqtSlot()
    def on_pa_cf_button_clicked(self):
        if self.heater['left']:
            self._printer.set_thermal('left', 300)
        if self.heater['right']:
            self._printer.set_thermal('right', 300)
        if self.heater['bed']:
            self._printer.set_thermal('bed', 90)
        if self.heater['chamber']:
            self._printer.set_thermal('chamber', 55)
        self.show_tips()
