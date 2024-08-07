from qtCore import *
from ui.components.base.baseLine import BaseHLine
from ui.components.filamentsWidget import FilamentsWidget
from ui.components.thermalWidget import ThermalWidget


class PreHeatWidget(QFrame):
    preheat_changed = pyqtSignal()

    def __init__(self, printer, parent, show_bed=True):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("PreHeatWidget")
        _height = 65 * 4 if show_bed else 65 * 3
        self.setFixedHeight(_height)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._thermal = ThermalWidget(self._printer, self._parent, show_bed=show_bed)
        self._thermal.thermalChanged.connect(self.on_thermal_user_changed)
        self._layout.addWidget(self._thermal)

        self._filament = FilamentsWidget(self._printer, have_bed=show_bed)
        self._filament.filamentChanged.connect(self.on_filaments_changed)
        self._layout.addWidget(self._filament)

        self._layout.addWidget(BaseHLine())

    @pyqtSlot()
    def on_thermal_user_changed(self):
        self.preheat_changed.emit()
        self._filament.set_filament_user()

    @pyqtSlot()
    def on_filaments_changed(self):
        self.preheat_changed.emit()

    def init_filaments(self):
        self._filament.set_filament_pla()

    def heat_again(self, wait=False):
        self._filament.set_filament(self._filament.filament, wait)

    def sync_thermal(self):
        self._filament.sync_thermal()
