from wlan import MixwareScreenWLAN

from qtCore import *
from ui.components.base.baseLine import BaseVLine, BaseHLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.base.baseRound import BaseRoundDialog


class WLANConnectBox(BaseRoundDialog):
    def __init__(self, wlan, parent):
        super().__init__(parent)
        self._wlan = wlan
        self._parent = parent
        self._width = self._parent._printer.config.get_width()
        self._height = self._parent._printer.config.get_height()

        self.resize(self._width - 40, self._height / 2)
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
        self.ssid_label = QLabel()
        self.ssid_label.setFixedHeight(40)
        self.ssid_label.setObjectName("message")
        self.ssid_label.setWordWrap(True)
        self.body_frame_layout.addWidget(self.ssid_label)
        self.ssid_line_edit = QLineEdit()
        self.ssid_line_edit.setFixedHeight(40)
        self.ssid_line_edit.setMaxLength(64)
        self.body_frame_layout.addWidget(self.ssid_line_edit)
        self.passwd_label = QLabel()
        self.passwd_label.setFixedHeight(40)
        self.body_frame_layout.addWidget(self.passwd_label)
        self.passwd_line_edit = QLineEdit()
        self.passwd_line_edit.setFixedHeight(40)
        self.passwd_line_edit.setMaxLength(64)
        self.passwd_line_edit.setEchoMode(QLineEdit.Password)
        self.passwd_line_edit_layout = QHBoxLayout(self.passwd_line_edit)
        self.passwd_line_edit_layout.setContentsMargins(1, 1, 1, 1)
        self.passwd_line_edit_layout.setSpacing(0)
        self.passwd_line_edit_layout.setAlignment(Qt.AlignRight)
        self.passwd_line_edit_button = BasePushButton(self.passwd_line_edit)
        self.passwd_line_edit_button.setIcon(QIcon("resource/icon/preview_close"))
        self.passwd_line_edit_button.setFixedSize(38, 38)
        self.passwd_line_edit_button.clicked.connect(self.on_passwd_line_edit_button_clicked)
        self.passwd_line_edit_layout.addWidget(self.passwd_line_edit_button)
        self.body_frame_layout.addWidget(self.passwd_line_edit)
        self.frame_layout.addWidget(self.body_frame)

        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(64)
        self.button_frame_layout = QHBoxLayout(self.footer_frame)
        self.button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.button_frame_layout.setSpacing(0)
        self.cancel_button = BasePushButton()
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_frame_layout.addWidget(self.cancel_button, 1)
        self.button_frame_layout.addWidget(BaseVLine())
        self.confirm_button = BasePushButton()
        self.confirm_button.clicked.connect(self.on_confirm)
        self.button_frame_layout.addWidget(self.confirm_button, 1)

        self.keyboard_frame = QFrame()
        self.keyboard_frame.setFixedSize(360, 180)
        self.keyboard_frame_layout = QVBoxLayout(self.keyboard_frame)
        self.keyboard_frame_layout.setContentsMargins(10, 10, 10, 50)
        self.keyboard_frame_layout.setSpacing(3)

        self.keyboard_button_group = QButtonGroup()
        self.keyboard_button_group.buttonClicked.connect(self.on_keyboard_button_clicked)
        self.keyboard_map = 0
        self.keys_list = \
            [
                ['q', 'Q', '0', '0'],
                ['w', 'W', '1', '1'],
                ['e', 'E', '2', '2'],
                ['r', 'R', '3', '3'],
                ['t', 'T', '4', '4'],
                ['y', 'Y', '5', '5'],
                ['u', 'U', '6', '6'],
                ['i', 'I', '7', '7'],
                ['o', 'O', '8', '8'],
                ['p', 'P', '9', '9']
            ], \
                [
                    ['a', 'A', '\\', '<'],
                    ['s', 'S', '/', '>'],
                    ['d', 'D', ':', '['],
                    ['f', 'F', ';', ']'],
                    ['g', 'G', '(', '{'],
                    ['h', 'H', ')', '}'],
                    ['j', 'J', '#', '#'],
                    ['k', 'K', '\&', '%'],
                    ['l', 'L', '@', '^']
                ], \
                [
                    'shift',
                    ['z', 'Z', '_', '*'],
                    ['x', 'X', '-', '+'],
                    ['c', 'C', '`', '='],
                    ['v', 'V', '?', '|'],
                    ['b', 'B', '!', '~'],
                    ['n', 'N', ',', '"'],
                    ['m', 'M', '.', '\''],
                    'delete',
                ], \
                ['?123', 'space', 'enter']

        for row_keys in self.keys_list:
            keyboard_layout = QHBoxLayout()
            keyboard_layout.setContentsMargins(0, 0, 0, 0)
            keyboard_layout.setSpacing(2)
            keyboard_layout.setAlignment(Qt.AlignCenter)
            for key in row_keys:
                keyboard_button = BasePushButton()
                keyboard_button.setFocusPolicy(Qt.NoFocus)
                if key == 'shift':
                    keyboard_button.setObjectName("keyboard_shift")
                    keyboard_button.setIcon(QIcon("resource/icon/shift.svg"))
                    keyboard_button.setFixedSize(48, 36)
                elif key == 'delete':
                    keyboard_button.setObjectName("keyboard_delete")
                    keyboard_button.setIcon(QIcon("resource/icon/delete.svg"))
                    keyboard_button.setFixedSize(48, 36)
                elif key == '?123':
                    keyboard_button.setObjectName("keyboard_?123")
                    keyboard_button.setText('?123')
                    keyboard_button.setFixedSize(54, 36)
                elif key == 'space':
                    keyboard_button.setObjectName("keyboard_space")
                    keyboard_button.setText(self.tr('Space'))
                    keyboard_button.setFixedSize(224, 36)
                elif key == 'enter':
                    keyboard_button.setObjectName("keyboard_enter")
                    keyboard_button.setIcon(QIcon("resource/icon/enter.svg"))
                    keyboard_button.setFixedSize(54, 36)
                else:
                    keyboard_button.setObjectName("keyboard_keys")
                    keyboard_button.setText(key[0])
                    keyboard_button.setFixedSize(32, 36)
                keyboard_button.setStyleSheet("border: 1px solid #5A5A5A; border-radius: 0;")
                if key == 'space':
                    self.keyboard_button_group.addButton(keyboard_button, 1)
                else:
                    self.keyboard_button_group.addButton(keyboard_button)
                keyboard_layout.addWidget(keyboard_button)
            self.keyboard_frame_layout.addLayout(keyboard_layout)

        self.frame_layout.addWidget(self.keyboard_frame)
        self.frame_layout.addWidget(BaseHLine())
        self.frame_layout.addWidget(self.footer_frame)
        self.keyboard_frame.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.frame)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.ssid_label.setText(self.tr("Network Name"))
        self.passwd_label.setText(self.tr("Password"))
        self.ssid_line_edit.setPlaceholderText(self.tr("Please input your network name."))
        self.passwd_line_edit.setPlaceholderText(self.tr("Please input your password."))
        self.title_label.setText(self.tr("Connect"))
        self.confirm_button.setText(self.tr("Connect"))
        self.cancel_button.setText(self.tr("Cancel"))
        self.keyboard_button_group.button(1).setText(self.tr('Space'))

    def show_keyborad(self):
        self.keyboard_frame.show()

    def re_keyboard_text(self, a0, a1):
        all_buttons = self.keyboard_button_group.buttons()
        for button in all_buttons:
            had_break = False
            if button.objectName() == "keyboard_keys":
                for row_keys in self.keys_list:
                    for key in row_keys:
                        if button.text() in key[a0]:
                            button.setText(key[a1])
                            had_break = True
                            break
                        if had_break: break
                    if had_break: break
        self.keyboard_map = a1

    def on_keyboard_button_clicked(self, button: QAbstractButton):
        object_name = button.objectName()
        if 'shift' in object_name:
            if self.keyboard_map == 0:
                self.re_keyboard_text(0, 1)
            elif self.keyboard_map == 1:
                self.re_keyboard_text(1, 0)
            elif self.keyboard_map == 2:
                self.re_keyboard_text(2, 3)
            elif self.keyboard_map == 3:
                self.re_keyboard_text(3, 2)
        elif 'delete' in object_name:
            if self.ssid_line_edit.hasFocus():
                current_passwd = self.ssid_line_edit.text()
                self.ssid_line_edit.setText(current_passwd[:-1])
            elif self.passwd_line_edit.hasFocus():
                current_passwd = self.passwd_line_edit.text()
                self.passwd_line_edit.setText(current_passwd[:-1])
        elif '?123' in object_name:
            if self.keyboard_map == 0 or self.keyboard_map == 1:
                button.setText('abc')
                self.re_keyboard_text(self.keyboard_map, 2)
            elif self.keyboard_map == 2 or self.keyboard_map == 3:
                self.re_keyboard_text(self.keyboard_map, 0)
                button.setText('?123')
        elif 'space' in object_name:
            if self.ssid_line_edit.hasFocus():
                self.ssid_line_edit.setText(self.ssid_line_edit.text() + ' ')
            elif self.passwd_line_edit.hasFocus():
                self.passwd_line_edit.setText(self.passwd_line_edit.text() + ' ')
        elif 'enter' in object_name:
            if self.ssid_line_edit.hasFocus():
                self.passwd_line_edit.setFocus()
            elif self.passwd_line_edit.hasFocus():
                self.on_confirm()
        else:
            if self.ssid_line_edit.hasFocus():
                self.ssid_line_edit.setText(self.ssid_line_edit.text() + button.text())
            elif self.passwd_line_edit.hasFocus():
                self.passwd_line_edit.setText(self.passwd_line_edit.text() + button.text())

    def on_passwd_line_edit_button_clicked(self):
        if self.passwd_line_edit.echoMode() == QLineEdit.Password:
            self.passwd_line_edit.setEchoMode(QLineEdit.Normal)
            self.passwd_line_edit_button.setIcon(QIcon("resource/icon/preview_open"))
        else:
            self.passwd_line_edit.setEchoMode(QLineEdit.Password)
            self.passwd_line_edit_button.setIcon(QIcon("resource/icon/preview_close"))

    def on_confirm(self):
        wlan.connect(self.ssid_line_edit.text(), self.passwd_line_edit.text())
        self.done(QMessageBox.Yes)

    def on_cancel(self):
        self.done(QMessageBox.Cancel)

    def set_name(self, text: str):
        self.ssid_line_edit.setText(text)

    def start(self, text=""):
        self.set_name(text)
        self.passwd_line_edit.clear()
        if text:
            self.passwd_line_edit.setFocus()
        else:
            self.ssid_line_edit.setFocus()
        self.exec()


class WlanBar(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, name="", security="", signal=0):
        super().__init__()
        self.is_move = None
        self.setObjectName("frameBox")
        self.setFixedSize(360, 92)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(0)
        self.frame = QFrame()
        self.frame.setFixedHeight(72)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.name = QLabel(name)
        self.name.setFixedHeight(40)
        self.frame_layout.addWidget(self.name)
        self.security = QLabel(security)
        self.security.setFixedHeight(32)
        self.security.setStyleSheet("QLabel {font-size: 17px; color: rgba(24, 24, 24, 0.5);}")
        self.frame_layout.addWidget(self.security)
        self.layout.addWidget(self.frame)
        self.signals = QLabel()
        self.signals.setFixedSize(72, 72)
        self.layout.addWidget(self.signals)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.clicked.emit(self.name.text())

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.is_move = True

    def set_name(self, name: str):
        self.name.setText(name)

    def set_security(self, security):
        self.security.setText(security)

    def set_signal(self, signals):
        self.signals.setText(f"{signals}%")


class WlanPage(QScrollArea):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("WlanPage")

        self.setStyleSheet("QScrollArea {border: none; background: transparent;}")
        self.setWidgetResizable(True)

        self.frame = QFrame()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout = QVBoxLayout(self.frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(10)
        self.setWidget(self.frame)

        self.connected_frame = QFrame()
        self.connected_frame_layout = QVBoxLayout(self.connected_frame)
        self.connected_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.connected_frame_layout.setSpacing(0)
        self.connected_title = QLabel()
        self.connected_frame_layout.addWidget(self.connected_title)
        self.connected_list_frame = QFrame()
        self.connected_list_frame_layout = QVBoxLayout(self.connected_list_frame)
        self.connected_list_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.connected_list_frame_layout.setSpacing(10)
        self.connected_frame_layout.addWidget(self.connected_list_frame)
        self.layout.addWidget(self.connected_frame)
        self.connected_frame.hide()

        self.available_frame = QFrame()
        self.available_frame_layout = QVBoxLayout(self.available_frame)
        self.available_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.available_frame_layout.setSpacing(0)
        self.available_title = QLabel()
        self.available_frame_layout.addWidget(self.available_title)
        self.available_list_frame = QFrame()
        self.available_list_frame_layout = QVBoxLayout(self.available_list_frame)
        self.available_list_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.available_list_frame_layout.setSpacing(10)
        self.available_frame_layout.addWidget(self.available_list_frame)
        self.layout.addWidget(self.available_frame)
        self.available_frame.hide()

        self.add_button = BasePushButton()
        self.add_button.setFixedHeight(64)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.layout.addWidget(self.add_button)

        wlan.newWlanList.connect(self.on_new_wlan_lists)
        self.wlan_connect_box = WLANConnectBox(wlan, self._parent)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(wlan.update)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()
        wlan.update()
        self.update_timer.start(15000)

    def hideEvent(self, a0: QHideEvent) -> None:
        self.update_timer.stop()

    def re_translate_ui(self):
        self.connected_title.setText(self.tr("Connected"))
        self.available_title.setText(self.tr("Available"))
        self.add_button.setText(self.tr("Add network"))

    def on_new_wlan_lists(self, lists):
        # delete old item
        for i in range(self.connected_list_frame_layout.count()):
            self.connected_list_frame_layout.itemAt(i).widget().deleteLater()
        self.connected_frame.hide()
        for i in range(self.available_list_frame_layout.count()):
            self.available_list_frame_layout.itemAt(i).widget().deleteLater()
        self.available_frame.hide()

        for _wlan in lists:
            # logging.info(f"find wlan:{_wlan}")
            if _wlan['in_use']:
                connected_bar = WlanBar(_wlan['ssid'], self.tr('Connected'), _wlan['signal'])
                self.connected_list_frame_layout.addWidget(connected_bar)
                if self.connected_frame.isHidden(): self.connected_frame.show()
            else:
                if _wlan['ssid']:
                    available_bar = WlanBar(_wlan['ssid'], _wlan['security'], _wlan['signal'])
                    available_bar.clicked.connect(self.on_available_bar_clicked)
                    self.available_list_frame_layout.addWidget(available_bar)
                    if self.available_frame.isHidden(): self.available_frame.show()

    def on_available_bar_clicked(self, name):
        self._parent.showShadowScreen()
        self.wlan_connect_box.start(name)
        self._parent.closeShadowScreen()

    def on_add_button_clicked(self):
        self._parent.showShadowScreen()
        self.wlan_connect_box.start()
        self._parent.closeShadowScreen()


wlan = MixwareScreenWLAN()
