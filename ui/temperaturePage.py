from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.printerPage import PrinterTemperatureWidget


class TemperaturePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("temperaturePage")

        self.frame = QFrame()
        self.add_button = BasePushButton()
        self.dec_button = BasePushButton()
        self.cool_button = BasePushButton()
        self.pla_button = BasePushButton()
        self.pa_cf_button = BasePushButton()

        self.temperatureWidget = PrinterTemperatureWidget(self._printer)
        self.temperature_group = QButtonGroup()
        self.heater = 'left'
        self.temperature_group.addButton(self.temperatureWidget.left, 0)
        self.temperature_group.addButton(self.temperatureWidget.right, 1)
        self.temperature_group.addButton(self.temperatureWidget.bed, 2)
        self.temperature_group.addButton(self.temperatureWidget.chamber, 3)

        self.degree_frame = QFrame()
        self.degree_title = QLabel()
        self.degree_group = QButtonGroup()
        self.degree_list = ["1", "5", "10", "20"]
        self.degree_default = "10"
        self.degree_current_id = 0

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.frame.setObjectName("frameBox")
        self.degree_frame.setObjectName("frameBox")
        self.degree_frame.setFixedHeight(88)
        self.frame.setStyleSheet("BasePushButton {border: 1px solid #D4D4D4;}")
        
        self.degree_title.setText(self.tr("Heating Degeee"))
        self.degree_title.setFixedHeight(40)
        self.degree_title.setStyleSheet("padding-left: 10px;")

        self.add_button.setText("+")
        self.dec_button.setText("-")
        self.pla_button.setText(self.tr("PLA"))
        self.pa_cf_button.setText(self.tr("PA-CF"))
        self.cool_button.setText(self.tr("Cool"))

    def initLayout(self):
        degree_frame_layout = QHBoxLayout(self.degree_frame)
        degree_frame_layout.setContentsMargins(5, 1, 5, 1)
        degree_frame_layout.setSpacing(0)
        for d in range(len(self.degree_list)):
            button = BasePushButton()
            button.setText(self.degree_list[d])
            button.setObjectName("dataButton")
            self.degree_group.addButton(button, d)
            if self.degree_list[d] == self.degree_default:
                self.on_degree_button_group_clicked(self.degree_group.button(d))
            degree_frame_layout.addWidget(button)

        degree_layout = QVBoxLayout()
        degree_layout.setContentsMargins(0, 0, 0, 0)
        degree_layout.setSpacing(0)
        degree_layout.addWidget(self.degree_title)
        degree_layout.addWidget(self.degree_frame)

        button_left_layout = QVBoxLayout()
        button_left_layout.addWidget(self.pla_button)
        button_left_layout.addWidget(self.pa_cf_button)
        button_left_layout.addWidget(self.cool_button)

        button_right_layout = QVBoxLayout()
        button_right_layout.addWidget(self.add_button)
        button_right_layout.addWidget(self.dec_button)

        button_layout = QHBoxLayout(self.frame)
        button_layout.addLayout(button_left_layout, 1)
        button_layout.addLayout(button_right_layout, 1)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)
        layout.addWidget(self.temperatureWidget, 5)
        layout.addLayout(degree_layout)
        layout.addWidget(self.frame, 4)

    def initConnect(self):
        self.degree_group.buttonClicked.connect(self.on_degree_button_group_clicked)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.dec_button.clicked.connect(self.on_dec_button_clicked)
        self.cool_button.clicked.connect(self.on_cool_button_clicked)
        self.pla_button.clicked.connect(self.on_pla_button_clicked)
        self.pa_cf_button.clicked.connect(self.on_pa_cf_button_clicked)

        self.temperature_group.idClicked.connect(self.on_temperature_button_group_clicked)

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

    def on_temperature_button_group_clicked(self, id):
        thermal = ['left', 'right', 'bed', 'chamber']
        if 0 <= id <= 3:
            self.heater = thermal[id]
            for i in range(4):
                if i == id:
                    self.temperature_group.button(i).setStyleSheet(checkedStyleSheet)
                else:
                    self.temperature_group.button(i).setStyleSheet(uncheckedStyleSheet)

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