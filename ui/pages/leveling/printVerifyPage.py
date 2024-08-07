import platform
import re

from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.baseTitleFrame import BaseTitleFrame
from ui.components.handleBar import HandleBar
from ui.components.messageBar import MessageBar
from ui.components.movieLabel import MovieLabel
from ui.components.preHeatWidget import PreHeatWidget
from ui.components.thermalWidget import ThermalWidget


class PrintVerifyPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.message_text_list = None
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._parent = parent

        self.setObjectName("printVerifyPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.reset_message_text()
        self.message_frame = BaseTitleFrame()
        self.message_list = self.message_frame.set_message(self.message_text_list)
        self.layout.addWidget(self.message_frame)

        self.handle_frame = QFrame()
        self.handle_frame.setFixedWidth(360)
        self.handle_frame.setObjectName("frameBox")
        self.handle_frame_layout = QVBoxLayout(self.handle_frame)
        self.handle_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.handle_frame_layout.setSpacing(10)
        self.handle_stacked_widget = QStackedWidget()
        self.handle_stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.remind_handle = HandleBar()
        self.remind_handle.previous_button.hide()
        self.remind_handle.next_button.clicked.connect(self.on_remind_next_button_clicked)
        self.remind_body_layout = QVBoxLayout(self.remind_handle.body)
        self.remind_body_layout.setContentsMargins(20, 0, 20, 0)
        self.remind_body_layout.setSpacing(0)
        self.remind_body_layout.setAlignment(Qt.AlignCenter)
        self.remind_logo = MovieLabel("resource/image/clean_bed.gif", 320, 320)
        self.remind_logo.setFixedSize(320, 320)
        self.remind_body_layout.addWidget(self.remind_logo)
        self.remind_text = QLabel()
        self.remind_text.setWordWrap(True)
        self.remind_text.setAlignment(Qt.AlignCenter)
        self.remind_body_layout.addWidget(self.remind_text)
        self.handle_stacked_widget.addWidget(self.remind_handle)

        self.preheat_handle = HandleBar()
        self.preheat_handle.previous_button.hide()
        self.preheat_handle.next_button.clicked.connect(self.on_preheat_next_button_clicked)
        self.preheat_body_layout = QVBoxLayout(self.preheat_handle.body)
        self.preheat_body_layout.setContentsMargins(20, 0, 20, 0)
        self.preheat_body_layout.setSpacing(0)

        self.preheat_filament = PreHeatWidget(self._printer, self._parent)
        self.preheat_filament.preheat_changed.connect(self.reset_preheat_handle_ui)
        self.preheat_body_layout.addWidget(self.preheat_filament)
        self.preheat_text = QLabel()
        self.preheat_text.setWordWrap(True)
        self.preheat_text.setAlignment(Qt.AlignCenter)
        self.preheat_body_layout.addWidget(self.preheat_text)
        self.handle_stacked_widget.addWidget(self.preheat_handle)

        self.work_handle = HandleBar()
        self.work_handle.previous_button.hide()
        self.work_handle.next_button.clicked.connect(self.on_clean_next_button_clicked)
        self.work_body_layout = QVBoxLayout(self.work_handle.body)
        self.work_body_layout.setContentsMargins(0, 0, 0, 0)
        # self.work_body_layout.setSpacing(0)

        self.work_frame = QFrame()
        self.work_frame_layout = QVBoxLayout(self.work_frame)
        self.work_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.work_frame_layout.setSpacing(0)
        self.work_thermal = ThermalWidget(self._printer, self._parent, show_bed=True)
        self.work_frame_layout.addWidget(self.work_thermal)

        self.verity_model_logo = QLabel()
        self.verity_model_logo.setFixedHeight(320)
        self.verity_model_logo.setAlignment(Qt.AlignCenter)
        self.verity_model_logo.setPixmap(QPixmap("resource/image/xy_verity").scaledToWidth(320))
        self.work_frame_layout.addWidget(self.verity_model_logo)
        self.work_text = QLabel()
        self.work_text.setWordWrap(True)
        self.work_text.setAlignment(Qt.AlignCenter)
        self.work_frame_layout.addWidget(self.work_text)

        self.work_baby_step_frame = QFrame()
        self.work_baby_step_frame.setObjectName("frameOutLine")
        self.work_baby_step_frame.setFixedHeight(64)
        self.work_baby_step_frame_layout = QHBoxLayout(self.work_baby_step_frame)
        self.work_baby_step_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.work_baby_step_frame_layout.setSpacing(0)
        self.work_baby_step_drop_button = BasePushButton()
        self.work_baby_step_drop_button.clicked.connect(self.on_work_baby_step_drop_button_clicked)
        self.work_baby_step_frame_layout.addWidget(self.work_baby_step_drop_button)
        self.work_baby_step_frame_layout.addWidget(BaseVLine())
        self.work_baby_step_lift_button = BasePushButton()
        self.work_baby_step_lift_button.clicked.connect(self.on_work_baby_step_lift_button_clicked)
        self.work_baby_step_frame_layout.addWidget(self.work_baby_step_lift_button)
        self.work_frame_layout.addWidget(self.work_baby_step_frame)
        self.work_body_layout.addWidget(self.work_frame)
        self.work_progress_bar = QProgressBar()
        self.work_progress_bar.setTextVisible(False)
        self.work_progress_bar.setFixedHeight(18)
        self.work_body_layout.addWidget(self.work_progress_bar)
        self.handle_stacked_widget.addWidget(self.work_handle)

        self.finished_handle = HandleBar()
        self.finished_handle.previous_button.hide()
        self.finished_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        self.finished_body_layout = QVBoxLayout(self.finished_handle.body)
        self.finished_body_layout.setContentsMargins(0, 20, 0, 0)
        self.finished_body_layout.setSpacing(0)
        self.verity_logo = MovieLabel("resource/image/verity.gif", 320, 320)
        self.verity_logo.setFixedHeight(320)
        self.finished_body_layout.addWidget(self.verity_logo)
        self.finished_text = QLabel()
        self.finished_text.setWordWrap(True)
        self.finished_text.setAlignment(Qt.AlignCenter)
        self.finished_body_layout.addWidget(self.finished_text)

        self.finished_distance_frame = QFrame()
        self.finished_distance_frame.setFixedHeight(128)
        self.finished_distance_frame_layout = QVBoxLayout(self.finished_distance_frame)
        self.finished_distance_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.finished_distance_frame_layout.setSpacing(0)
        self.finished_distance_title = QLabel()
        self.finished_distance_title.setObjectName("frame_title")
        self.finished_distance_title.setFixedHeight(40)
        self.finished_distance_frame_layout.addWidget(self.finished_distance_title)
        self.finished_distance_button_frame = QFrame()
        self.finished_distance_button_frame.setObjectName("frameOutLine")
        self.finished_distance_button_frame.setFixedHeight(72)
        self.finished_distance_button_frame_layout = QHBoxLayout(self.finished_distance_button_frame)
        self.finished_distance_button_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.finished_distance_button_frame_layout.setSpacing(0)
        self._button_group = QButtonGroup()
        self._button_group.buttonClicked.connect(self.on_offset_distance_button_clicked)
        self._distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self._distance_default = "0.1"
        self._distance_current_id = 0
        for d in range(len(self._distance_list)):
            button = BasePushButton()
            button.setText(self._distance_list[d])
            self._button_group.addButton(button, d)
            if self._distance_list[d] == self._distance_default:
                self.on_offset_distance_button_clicked(
                    self._button_group.button(d))
            self.finished_distance_button_frame_layout.addWidget(button)
        self.finished_distance_frame_layout.addWidget(self.finished_distance_button_frame)
        self.finished_body_layout.addWidget(self.finished_distance_frame)
        self.finished_offset_frame = QFrame()
        self.finished_offset_frame.setFixedHeight(168)
        self.finished_offset_frame_layout = QGridLayout(self.finished_offset_frame)
        self.finished_offset_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.finished_offset_frame_layout.setSpacing(0)
        self.finished_offset_x_label = QLabel()
        self.finished_offset_x_label.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_label, 0, 0, 1, 2)
        self.finished_offset_x_dec_button = QPushButton()
        self.finished_offset_x_dec_button.setObjectName("leftLogo")
        # self.finished_offset_x_dec_button.setFixedHeight(56)
        self.finished_offset_x_dec_button.clicked.connect(self.on_finished_offset_x_dec_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_dec_button, 0, 2, 1, 1)
        self.finished_offset_x_add_button = QPushButton()
        self.finished_offset_x_add_button.setObjectName("rightLogo")
        # self.finished_offset_x_add_button.setFixedHeight(56)
        self.finished_offset_x_add_button.clicked.connect(self.on_finished_offset_x_add_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_add_button, 0, 3, 1, 1)
        self.finished_offset_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 4)
        self.finished_offset_y_label = QLabel()
        self.finished_offset_y_label.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_label, 2, 0, 1, 2)
        self.finished_offset_y_dec_button = QPushButton()
        self.finished_offset_y_dec_button.setObjectName("downLogo")
        # self.finished_offset_y_dec_button.setFixedHeight(56)
        self.finished_offset_y_dec_button.clicked.connect(self.on_finished_offset_y_add_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_dec_button, 2, 2, 1, 1)
        self.finished_offset_y_add_button = QPushButton()
        self.finished_offset_y_add_button.setObjectName("upLogo")
        # self.finished_offset_y_add_button.setFixedHeight(56)
        self.finished_offset_y_add_button.clicked.connect(self.on_finished_offset_y_dec_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_add_button, 2, 3, 1, 1)
        self.finished_body_layout.addWidget(self.finished_offset_frame)
        # self.finished_body_layout.addWidget(BaseHLine())

        self.handle_stacked_widget.addWidget(self.finished_handle)
        self.handle_frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def hideEvent(self, a0):
        # if self._printer.get_target('right')
        pass

    def reset_message_text(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Working."),
            self.tr("Finish.")
        ]

    def reset_ui(self):
        self.reset_message_text()
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def re_translate_ui(self):
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 220°C)"))
        self.work_text.setText(self.tr("Verification model printing, please wait."))
        self.work_baby_step_lift_button.setText(self.tr("Lift Bed"))
        self.work_baby_step_drop_button.setText(self.tr("Drop Bed"))
        self.finished_handle.next_button.setText(self.tr("Done"))
        self.finished_distance_title.setText(self.tr("Move Distance (mm)"))
        self.finished_text.setText(self.tr(
            "Observe the XY test model, find aligned lines, with each grid measuring 0.1mm, and adjust the offset values of the left and right nozzles."))

        self.finished_offset_x_label.setText("X: 0.0")
        self.finished_offset_y_label.setText("Y: 0.0")

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        if self._printer.is_print_verify():
            self.work_progress_bar.setValue(int(self._printer.print_progress() * 100))
        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170 \
                    and self._printer.get_temperature('bed') + 3 >= self._printer.get_target('bed'):
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if not self.isVisible():
            return
        if state == MixwareScreenPrinterStatus.PRINTER_VERITY:
            self.work_thermal.hide()
            self.verity_model_logo.hide()
            self.work_baby_step_frame.hide()
            self.work_text.setText(self.tr("Printing is completed."))
            self.work_handle.next_button.setEnabled(True)

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)

    @pyqtSlot(QAbstractButton)
    def on_offset_distance_button_clicked(self, button):
        if button.text() in self._distance_list:
            if self._button_group.id(button) != self._distance_current_id:
                update_style(self._button_group.button(self._distance_current_id), "unchecked")
                update_style(self._button_group.button(self._button_group.id(button)), "checked")
                self._distance_current_id = self._button_group.id(button)

    def on_remind_next_button_clicked(self):
        if is_release:
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        self.preheat_filament.init_filaments()
        self._printer.write_gcode_command("M155 S1")
        self._printer.auto_home()
        self._printer.write_gcode_command("T0")
        self._printer.move_to_xy(0, 20)
        self._printer.move_to_z(50)
        self._printer.write_gcode_command("M155 S0")

    def reset_preheat_handle_ui(self):
        if self.preheat_handle.next_button.isEnabled():
            self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 220°C)"))
            self.preheat_handle.next_button.setEnabled(False)

    def on_preheat_next_button_clicked(self):
        self.work_handle.next_button.setEnabled(False)
        self._parent.footer.setEnabled(False)
        self._printer.print_verify()
        self.goto_next_step_stacked_widget()

    def on_clean_next_button_clicked(self):
        self._printer.auto_home()
        self._printer.move_to_xy(190, 20, wait=True)
        self._printer.move_to_z(150, wait=True)
        self.goto_next_step_stacked_widget()
        self._parent.footer.setEnabled(True)
        self.finished_handle.next_button.setText(self.tr("Done."))

    def on_finished_offset_x_dec_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        offset = float(text[0])
        offset += float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        offset = float('%.2f' % offset)
        self.finished_offset_x_label.setText(f"X: {offset}")

    def on_finished_offset_x_add_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        offset = float(text[0])
        offset -= float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        offset = float('%.2f' % offset)
        self.finished_offset_x_label.setText(f"X: {offset}")

    def on_finished_offset_y_dec_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        offset = float(text[0])
        offset -= float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        offset = float('%.2f' % offset)
        self.finished_offset_y_label.setText(f"Y: {offset}")

    def on_finished_offset_y_add_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        offset = float(text[0])
        offset += float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        offset = float('%.2f' % offset)
        self.finished_offset_y_label.setText(f"Y: {offset}")

    def on_finished_next_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        hotend_offset_x = float(text[0])
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        hotend_offset_y = float(text[0])
        self._printer.set_hotend_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            hotend_offset_x))
        self._printer.set_hotend_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            hotend_offset_y))
        self.reset_ui()
        self._parent.gotoPreviousPage()

    def on_work_baby_step_lift_button_clicked(self):
        self._printer.baby_step_lift(0.1)

    def on_work_baby_step_drop_button_clicked(self):
        self._printer.baby_step_drop(0.1)
