from qtCore import *
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.base.baseRound import BaseRoundDialog
from ui.pages.printFilePage import PrintFilePage


class VerityMessageBox(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self.preheat_filament = None
        self._printer = printer
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()

        self.resize(self._width - 40, self._height / 3)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; }")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")

        self.title_frame_layout = QHBoxLayout(self.title_frame)
        self.title_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.title_frame_layout.setSpacing(0)

        self.title_label = QLabel()
        self.title_frame_layout.addWidget(self.title_label)

        self.title_close_button = BasePushButton()
        self.title_close_button.setText("x")
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.clicked.connect(self.on_cancel)
        self.title_frame_layout.addWidget(self.title_close_button)
        self.frame_layout.addWidget(self.title_frame)

        self.body_frame = QFrame()
        self.body_frame_layout = QVBoxLayout(self.body_frame)
        self.body_frame_layout.setAlignment(Qt.AlignCenter)
        self.body_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.body_frame_layout.setSpacing(0)

        self.message_label = QLabel()
        self.message_label.setFixedHeight(128)
        self.message_label.setObjectName("message")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.body_frame_layout.addWidget(self.message_label)
        self.tips_label = QLabel()
        self.tips_label.setFixedHeight(40)
        self.tips_label.setObjectName("tips")
        self.body_frame_layout.addWidget(self.tips_label)
        self.body_frame_layout.addWidget(BaseHLine())
        self.preheat_filament_layout = QHBoxLayout()
        self.preheat_filament_layout.setContentsMargins(0, 0, 0, 0)
        self.preheat_filament_layout.setSpacing(0)
        self.preheat_pla = BasePushButton()
        self.preheat_pla.setFixedHeight(64)
        self.preheat_pla.clicked.connect(self.on_preheat_pla_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pla)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_abs = BasePushButton()
        self.preheat_abs.setFixedHeight(64)
        self.preheat_abs.clicked.connect(self.on_preheat_abs_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_abs)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_pet = BasePushButton()
        self.preheat_pet.setFixedHeight(64)
        self.preheat_pet.clicked.connect(self.on_preheat_pet_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pet)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_pa = BasePushButton()
        self.preheat_pa.setFixedHeight(64)
        self.preheat_pa.clicked.connect(self.on_preheat_pa_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pa)
        self.body_frame_layout.addLayout(self.preheat_filament_layout)
        self.body_frame_layout.addWidget(BaseHLine())

        self.frame_layout.addWidget(self.body_frame)
        self.frame_layout.addWidget(BaseHLine())
        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(64)
        self.button_frame_layout = QHBoxLayout(self.footer_frame)
        self.button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.button_frame_layout.setSpacing(0)
        self.cancel_button = BasePushButton()
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_frame_layout.addWidget(self.cancel_button, 1)
        self.button_line = BaseVLine()
        self.button_frame_layout.addWidget(self.button_line)
        self.confirm_button = BasePushButton()
        self.confirm_button.clicked.connect(self.on_confirm)
        self.button_frame_layout.addWidget(self.confirm_button, 1)
        self.frame_layout.addWidget(self.footer_frame)
        self.layout.addWidget(self.frame)

    def on_confirm(self):
        self._printer.write_gcode_command(
            f"M104 T0 S{self.preheat_filament}\nM104 T1 S{self.preheat_filament}\nM190 S60\nM109 T0 S{self.preheat_filament}\nM109 T1 S{self.preheat_filament}")
        self.done(QMessageBox.Yes)

    def on_cancel(self):
        self.done(QMessageBox.Cancel)

    def on_preheat_pla_clicked(self):
        update_style(self.preheat_pla, "checked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")
        self.preheat_filament = 210

    def on_preheat_abs_clicked(self):
        self.preheat_filament = 240
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "checked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")

    def on_preheat_pet_clicked(self):
        self.preheat_filament = 270
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "checked")

    def on_preheat_pa_clicked(self):
        self.preheat_filament = 300
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "checked")
        update_style(self.preheat_pet, "unchecked")

    def start(self) -> int:
        self.title_label.setText("Mixware Screen")
        self.message_label.setText(self.tr("Whether to print the 'XY Offset Calibration' model?"))
        self.tips_label.setText(self.tr("Select the filament heating temperature"))
        self.confirm_button.setText(self.tr("Confirm"))
        self.cancel_button.setText(self.tr("Cancel"))
        self.preheat_pla.setText("PLA")
        self.preheat_abs.setText("ABS")
        self.preheat_pet.setText("PET")
        self.preheat_pa.setText("PA")
        self.on_preheat_pla_clicked()
        return self.exec()


class PrintPreparePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("printPreParePage")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.usb_button = BasePushButton()
        self.layout.addWidget(self.usb_button, 0, 0, 1, 2)

        self.xy_button = BasePushButton()
        self.xy_button.clicked.connect(self.print_xy_verity)
        self.layout.addWidget(self.xy_button, 1, 0)

        self.local_button = BasePushButton()
        self.layout.addWidget(self.local_button, 1, 1)

        self.printFilePage = PrintFilePage(self._printer, self._parent)
        QScroller.grabGesture(self.printFilePage, QScroller.TouchGesture)

        self.verityMessageBox = VerityMessageBox(self._printer)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.local_button.setText(self.tr("Local Print"))
        self.usb_button.setText(self.tr("USB Print"))
        self.xy_button.setText(self.tr("XY Offset\nCalibration"))

    @pyqtSlot()
    def print_xy_verity(self):
        self._parent.showShadowScreen()
        ret = self.verityMessageBox.start()
        if ret == QMessageBox.Yes:
            self._printer.print_start('resource/gcodes/print_verify.gcode')
        self._parent.closeShadowScreen()
