from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.levelPages.autoLevelPage import AutoLevelPage
from ui.levelPages.bedLevelPage import BedLevelPage
from ui.levelPages.dialIndicatorPage import DialIndicatorPage
from ui.levelPages.offsetPage import OffsetPage
from ui.levelPages.printVerifyPage import PrintVerifyPage


class LevelPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("levelPage")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.bed_level = BasePushButton()
        self.bed_level.clicked.connect(self.goto_bed_level_page)
        self.layout.addWidget(self.bed_level, 0, 0)
        self.bed_mesh = BasePushButton()
        self.bed_mesh.clicked.connect(self.goto_auto_level_page)
        self.layout.addWidget(self.bed_mesh, 0, 1)
        self.offset_z = BasePushButton()
        self.offset_z.clicked.connect(self.goto_offset_z_page)
        self.layout.addWidget(self.offset_z, 1, 0)
        self.offset_xy = BasePushButton()
        self.offset_xy.clicked.connect(self.goto_offset_xy_page)
        self.layout.addWidget(self.offset_xy, 1, 1)
        self.offset = BasePushButton()
        self.offset.clicked.connect(self.goto_offset_page)
        self.layout.addWidget(self.offset, 2, 0)

        self.bedLevelPage = BedLevelPage(self._printer, self._parent)
        self.autoLevelPage = AutoLevelPage(self._printer, self._parent)
        self.offsetPage = OffsetPage(self._printer, self._parent)
        self.dialIndicatorPage = DialIndicatorPage(self._printer, self._parent)
        self.printVerifyPage = PrintVerifyPage(self._printer, self._parent)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.bed_level.setText(self.tr("Bed Leveling"))
        self.bed_mesh.setText(self.tr("Auto-leveling"))
        self.offset.setText(self.tr("Adjust Offset"))
        self.offset_z.setText(self.tr("Right Extruder\nHeight Calibration"))
        self.offset_xy.setText(self.tr("XY Offset\nCalibration"))

    @pyqtSlot()
    def goto_auto_level_page(self):
        self._parent.gotoPage(self.autoLevelPage, self.tr("Auto-leveling"))

    @pyqtSlot()
    def goto_bed_level_page(self):
        self._parent.gotoPage(self.bedLevelPage, self.tr("Bed Leveling"))

    @pyqtSlot()
    def goto_offset_page(self):
        self._parent.gotoPage(self.offsetPage, self.tr("Adjust Offset"))

    @pyqtSlot()
    def goto_offset_z_page(self):
        self._parent.gotoPage(self.dialIndicatorPage, self.tr("Right Extruder Height Calibration"))

    @pyqtSlot()
    def goto_offset_xy_page(self):
        self._parent.gotoPage(self.printVerifyPage, self.tr("XY Offset Calibration"))
