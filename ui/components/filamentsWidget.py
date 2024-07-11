import logging

from qtCore import *
from ui.components.base.baseLine import BaseVLine
from ui.components.base.basePushButton import BasePushButton


class FilamentsWidget(QFrame):
    filamentChanged = pyqtSignal()

    def __init__(self, printer, show_line=True):
        super().__init__()
        self._filament = 'user'
        self._target_left = 0
        self._target_right = 0
        self._target_bed = 0
        self._printer = printer
        self._show_line = show_line

        self.setObjectName("FilamentsWidget")
        self.setFixedHeight(64)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._pla_button = BasePushButton()
        self._pla_button.clicked.connect(self.set_filament_pla)
        self._layout.addWidget(self._pla_button)

        if self._show_line:
            self._layout.addWidget(BaseVLine())

        self._abs_button = BasePushButton()
        self._abs_button.clicked.connect(self.set_filament_abs)
        self._layout.addWidget(self._abs_button)

        if self._show_line:
            self._layout.addWidget(BaseVLine())

        self._pet_button = BasePushButton()
        self._pet_button.clicked.connect(self.set_filament_pet)
        self._layout.addWidget(self._pet_button)

        if self._show_line:
            self._layout.addWidget(BaseVLine())

        self._pa_button = BasePushButton()
        self._pa_button.clicked.connect(self.set_filament_pa)
        self._layout.addWidget(self._pa_button)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self._pla_button.setText("PLA")
        self._abs_button.setText("ABS")
        self._pet_button.setText("PET")
        self._pa_button.setText("PA")

    def sync_thermal(self):
        if self._filament == 'user':
            self._target_left = self._printer.get_target('left')
            self._target_right = self._printer.get_target('right')
            self._target_bed = self._printer.get_target('bed')

    def reset_filaments_style(self):
        update_style(self._pla_button, "unchecked")
        update_style(self._abs_button, "unchecked")
        update_style(self._pet_button, "unchecked")
        update_style(self._pa_button, "unchecked")

    def set_filament(self, filament, wait=False):
        if type(filament) == str:
            if filament == 'pla':
                self._filament = 'pla'
                self._target_left = self._target_right = 220
                self._target_bed = 60
            elif filament == 'abs':
                self._filament = 'abs'
                self._target_left = self._target_right = 250
                self._target_bed = 60
            elif filament == 'pet':
                self._filament = 'pet'
                self._target_left = self._target_right = 290
                self._target_bed = 75
            elif filament == 'pa':
                self._filament = 'pa'
                self._target_left = self._target_right = 300
                self._target_bed = 75
        elif type(filament) == tuple:
            if len(filament) == 2:
                self._filament = 'user'
                self._target_left = filament[0]
                self._target_right = filament[1]
            elif len(filament) == 3:
                self._filament = 'user'
                self._target_left = filament[0]
                self._target_right = filament[1]
                self._target_bed = filament[2]
        else:
            return

        self._printer.set_thermal('left', self._target_left)
        self._printer.set_thermal('right', self._target_right)
        self._printer.set_thermal('bed', self._target_bed)

        if wait:
            self._printer.write_gcode_commands(f"M109 T0 S{self._target_left}\nM109 T1 S{self._target_right}")

        logging.debug(
            F'Preheat {self._filament} : {self._target_left} - {self._target_right} - {self._target_bed}')

    def set_filament_pla(self):
        self.set_filament('pla')
        self.reset_filaments_style()
        update_style(self._pla_button, "checked")
        self.filamentChanged.emit()

    def set_filament_abs(self):
        self.set_filament('abs')
        self.reset_filaments_style()
        update_style(self._abs_button, "checked")
        self.filamentChanged.emit()

    def set_filament_pet(self):
        self.set_filament('pet')
        self.reset_filaments_style()
        update_style(self._pet_button, "checked")
        self.filamentChanged.emit()

    def set_filament_pa(self):
        self.set_filament('pa')
        self.reset_filaments_style()
        update_style(self._pa_button, "checked")
        self.filamentChanged.emit()

    def set_filament_user(self):
        self._filament = 'user'
        self.reset_filaments_style()
        self.filamentChanged.emit()

    @property
    def filament(self):
        return self._filament
