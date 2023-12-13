from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.levelPages.bedMeshGraph import BedMeshGraph


class AutoLevelPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)

        self.setObjectName("autoLevelPage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignCenter)

        self.tips = QLabel()
        self.tips.setAlignment(Qt.AlignCenter)
        self.tips.setFixedSize(360, 128)
        self.layout.addWidget(self.tips)

        self.bed_mesh_graph = BedMeshGraph()
        self.layout.addWidget(self.bed_mesh_graph)

        self.start_button = BasePushButton()
        self.start_button.setFixedHeight(64)
        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.layout.addWidget(self.start_button)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.bed_mesh_graph.show_bed_mesh(self._printer.information['bedMesh'])
        self.tips.setText("Auto bed leveling, please wait.")
        self.start_button.setText(self.tr("Start Auto-level"))
        self.bed_mesh_graph.show()
        self.start_button.show()
        self.tips.hide()

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if state == MixwareScreenPrinterStatus.PRINTER_G29:
            self.re_translate_ui()
            self.tips.setText("Auto bed level done.")
            self.tips.show()

    @pyqtSlot()
    def on_start_button_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start("Mixware Screen", "Start Auto bed level?", buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('G28\nD28\nG29\nM500\nM503')
            self.tips.show()
            self.bed_mesh_graph.hide()
            self.start_button.hide()
        self._parent.closeShadowScreen()
