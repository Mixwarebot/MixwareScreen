from qtCore import *
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar


class NozzlePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.message_text_list = None
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self._parent = parent

        self.setObjectName("nozzlePage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        self.message_frame.setFixedHeight(240)
        self.message_layout = QVBoxLayout(self.message_frame)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(10)
        self.message_list = []
        self.reset_message_text()
        for i in range(len(self.message_text_list)):
            self.message_list.append(MessageBar(i + 1, self.message_text_list[i]))
            self.message_layout.addWidget(self.message_list[i])
        self.layout.addWidget(self.message_frame)

        self.handle_frame = QFrame()
        # self.handle_frame.setFixedWidth(360)
        self.handle_frame.setObjectName("frameBox")
        self.handle_frame_layout = QVBoxLayout(self.handle_frame)
        self.handle_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.handle_frame_layout.setSpacing(10)
        self.handle_stacked_widget = QStackedWidget()
        self.handle_stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.start_handle = HandleBar()
        self.start_handle.previous_button.hide()
        self.start_handle.next_button.clicked.connect(self.on_start_next_button_clicked)
        self.start_body_layout = QVBoxLayout(self.start_handle.body)
        self.start_body_layout.setContentsMargins(20, 0, 20, 0)
        self.start_body_layout.setSpacing(0)
        self.start_body_layout.setAlignment(Qt.AlignCenter)
        self.start_text = QLabel()
        self.start_text.setMinimumHeight(360)
        self.start_text.setWordWrap(True)
        # self.start_text.setAlignment(Qt.AlignCenter)
        self.start_body_layout.addWidget(self.start_text)
        self.handle_stacked_widget.addWidget(self.start_handle)

        self.step_1_handle = HandleBar()
        self.step_1_handle.previous_button.hide()
        self.step_1_handle.next_button.clicked.connect(self.on_step_1_next_button_clicked)
        self.step_1_body_layout = QVBoxLayout(self.step_1_handle.body)
        self.step_1_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_1_body_layout.setSpacing(0)
        self.step_1_body_layout.setAlignment(Qt.AlignCenter)
        self.step_1_logo = QLabel()
        self.step_1_logo.setFixedSize(320, 360)
        self.step_1_logo.setPixmap(QPixmap("resource/image/replace_nozzle_1.png").scaledToWidth(320))
        self.step_1_body_layout.addWidget(self.step_1_logo)
        self.step_1_text = QLabel()
        self.step_1_text.setWordWrap(True)
        self.step_1_text.setAlignment(Qt.AlignCenter)
        self.step_1_body_layout.addWidget(self.step_1_text)
        self.handle_stacked_widget.addWidget(self.step_1_handle)

        self.step_2_handle = HandleBar()
        self.step_2_handle.previous_button.hide()
        self.step_2_handle.next_button.clicked.connect(self.on_step_2_next_button_clicked)
        self.step_2_body_layout = QVBoxLayout(self.step_2_handle.body)
        self.step_2_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_2_body_layout.setSpacing(0)
        self.step_2_body_layout.setAlignment(Qt.AlignCenter)
        self.step_2_logo = QLabel()
        self.step_2_logo.setFixedSize(320, 320)
        self.step_2_logo.setPixmap(QPixmap("resource/image/replace_nozzle_2.png").scaledToWidth(320))
        self.step_2_body_layout.addWidget(self.step_2_logo)
        self.step_2_text = QLabel()
        self.step_2_text.setWordWrap(True)
        self.step_2_text.setAlignment(Qt.AlignCenter)
        self.step_2_body_layout.addWidget(self.step_2_text)
        self.handle_stacked_widget.addWidget(self.step_2_handle)

        self.step_3_handle = HandleBar()
        self.step_3_handle.previous_button.hide()
        self.step_3_handle.next_button.clicked.connect(self.on_step_3_next_button_clicked)
        self.step_3_body_layout = QVBoxLayout(self.step_3_handle.body)
        self.step_3_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_3_body_layout.setSpacing(0)
        self.step_3_body_layout.setAlignment(Qt.AlignCenter)
        self.step_3_logo = QLabel()
        self.step_3_logo.setFixedSize(320, 360)
        self.step_3_logo.setPixmap(QPixmap("resource/image/replace_nozzle_3.png").scaledToWidth(320))
        self.step_3_body_layout.addWidget(self.step_3_logo)
        self.step_3_text = QLabel()
        self.step_3_text.setWordWrap(True)
        self.step_3_text.setAlignment(Qt.AlignCenter)
        self.step_3_body_layout.addWidget(self.step_3_text)
        self.handle_stacked_widget.addWidget(self.step_3_handle)

        self.step_4_handle = HandleBar()
        self.step_4_handle.previous_button.hide()
        self.step_4_handle.next_button.clicked.connect(self.on_step_4_next_button_clicked)
        self.step_4_body_layout = QVBoxLayout(self.step_4_handle.body)
        self.step_4_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_4_body_layout.setSpacing(0)
        self.step_4_body_layout.setAlignment(Qt.AlignCenter)
        self.step_4_logo = QLabel()
        self.step_4_logo.setFixedSize(320, 360)
        self.step_4_logo.setPixmap(QPixmap("resource/image/replace_nozzle_4.png").scaledToWidth(320))
        self.step_4_body_layout.addWidget(self.step_4_logo)
        self.step_4_text = QLabel()
        self.step_4_text.setWordWrap(True)
        self.step_4_text.setAlignment(Qt.AlignCenter)
        self.step_4_body_layout.addWidget(self.step_4_text)
        self.handle_stacked_widget.addWidget(self.step_4_handle)

        self.step_5_handle = HandleBar()
        self.step_5_handle.previous_button.hide()
        self.step_5_handle.next_button.clicked.connect(self.on_step_5_next_button_clicked)
        self.step_5_body_layout = QVBoxLayout(self.step_5_handle.body)
        self.step_5_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_5_body_layout.setSpacing(0)
        self.step_5_body_layout.setAlignment(Qt.AlignCenter)
        self.step_5_logo = QLabel()
        self.step_5_logo.setFixedSize(320, 360)
        self.step_5_logo.setPixmap(QPixmap("resource/image/replace_nozzle_5.png").scaledToWidth(320))
        self.step_5_body_layout.addWidget(self.step_5_logo)
        self.step_5_text = QLabel()
        self.step_5_text.setWordWrap(True)
        self.step_5_text.setAlignment(Qt.AlignCenter)
        self.step_5_body_layout.addWidget(self.step_5_text)
        self.handle_stacked_widget.addWidget(self.step_5_handle)

        self.step_6_handle = HandleBar()
        self.step_6_handle.previous_button.hide()
        self.step_6_handle.next_button.clicked.connect(self.on_step_6_next_button_clicked)
        self.step_6_body_layout = QVBoxLayout(self.step_6_handle.body)
        self.step_6_body_layout.setContentsMargins(20, 0, 20, 0)
        self.step_6_body_layout.setSpacing(0)
        self.step_6_body_layout.setAlignment(Qt.AlignCenter)
        self.step_6_logo = QLabel()
        self.step_6_logo.setFixedSize(320, 360)
        self.step_6_logo.setPixmap(QPixmap("resource/image/replace_nozzle_6.png").scaledToWidth(320))
        self.step_6_body_layout.addWidget(self.step_6_logo)
        self.step_6_text = QLabel()
        self.step_6_text.setWordWrap(True)
        self.step_6_text.setAlignment(Qt.AlignCenter)
        self.step_6_body_layout.addWidget(self.step_6_text)
        self.handle_stacked_widget.addWidget(self.step_6_handle)

        self.handle_frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def re_translate_ui(self):
        self.start_handle.next_button.setText(self.tr("I'm ready."))
        self.start_text.setText(self.tr(
            "- If the nozzle assembly does not work properly, please cut the printing wire above the extruder to facilitate the removal of the nozzle assembly.\n\n"
            "- If the nozzle assembly is working properly, please unload the printing filament through the return process first.\n\n\n"
            "Note: Please ensure that the nozzle temperature is ≤50°C before operation to avoid burns."))
        self.step_1_text.setText(
            self.tr("Use a hex wrench to loosen the two jack screws on the radiator without removing them."))
        self.step_2_text.setText(self.tr("Unplug the <Heating Tube> and <Thermometer> on the extruder."))
        self.step_3_text.setText(self.tr(
            "Move the <Pressure Lever> to one side and remove the <Nozzle Assembly> downwards from the radiator."))
        self.step_4_text.setText(self.tr("Push the new <Nozzle Assembly> into the radiator from below until it stops."))
        self.step_5_text.setText(
            self.tr("Insert the plugs of the <Heating Tube> and <Thermometer> into the corresponding sockets."))
        self.step_6_text.setText(self.tr("Use a hex wrench to tighten the two jack screws on the radiator."))

    @pyqtSlot()
    def on_update_printer_information(self):
        pass

    def reset_ui(self):
        self.reset_message_text()
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
            if count < 3:
                self.message_list[count].show()
            else:
                self.message_list[count].hide()
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def reset_message_text(self):
        self.message_text_list = [
            self.tr("Replacement preparation.."),
            self.tr("Loosen the screw."),
            self.tr("Pull the plug out of the socket."),
            self.tr("Remove the nozzle assembly."),
            self.tr("Load the nozzle assembly."),
            self.tr("Insert the plug into the socket."),
            self.tr("Tighten the screws.")
        ]

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)
            if 0 < index < (self.handle_stacked_widget.count() - 2):
                self.message_list[index - 1].hide()
                self.message_list[index + 2].show()

    def on_start_next_button_clicked(self):
        self._printer.write_gcode_commands("G28\nG1 F8400 Y20\nM84")
        self.goto_next_step_stacked_widget()

    def on_step_1_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_step_2_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_step_3_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_step_4_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_step_5_next_button_clicked(self):
        self.goto_next_step_stacked_widget()
        self.step_6_handle.next_button.setText(self.tr("Done."))

    def on_step_6_next_button_clicked(self):
        self._parent.gotoPreviousPage()
