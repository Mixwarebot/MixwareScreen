from qtCore import *
from ui.pages.base.basePrintWidget import BasePrintWidget
from ui.pages.welcomePages.usePreparePage import UsePreparePage
from ui.pages.wlanPage import WlanPage


class WelcomeMainPage(BasePrintWidget):
    updateTranslator = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self.current_index = 0
        self._page_list = []
        self._printer = printer

        self.setObjectName("welcomeMainPage")
        self.header.clicked.disconnect()
        self.footer.hide()

        self.next_button = QPushButton(self)
        self.next_button.setFixedSize(84, 52)
        self.next_button.move(self.width() - self.next_button.width() - 20, 18)
        self.next_button.clicked.connect(self.on_next_button_clicked)

        self.body_frame = QFrame()
        self.body_frame_layout = QStackedLayout(self.body_frame)
        self.body_frame_layout.setContentsMargins(0, 0, 0, 0)
        # select language
        self.language_frame = QFrame()
        self.language_frame.setObjectName('languageFrame')
        self.language_frame_layout = QVBoxLayout(self.language_frame)
        self.language_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.language_frame_layout.setSpacing(10)
        self.language_frame_layout.setAlignment(Qt.AlignTop)
        self.language_e = QPushButton("English")
        self.language_e.setFixedHeight(64)
        self.language_e.setObjectName("checked")
        self.language_e.clicked.connect(self.on_language_e_clicked)
        self.language_frame_layout.addWidget(self.language_e)
        self.language_c = QPushButton("简体中文")
        self.language_c.setFixedHeight(64)
        self.language_c.setObjectName("unchecked")
        self.language_c.clicked.connect(self.on_language_c_clicked)
        self.language_frame_layout.addWidget(self.language_c)
        self.body_frame_layout.addWidget(self.language_frame)
        # wlan connect
        self.wlan_frame = WlanPage(self._printer, self)
        self.wlan_frame.setObjectName('wlanPage')
        self.body_frame_layout.addWidget(self.wlan_frame)
        # load filament
        self.usePreparePage = UsePreparePage(self._printer, self)
        self.usePreparePage.setObjectName('usePreparePage')
        self.body_frame_layout.addWidget(self.usePreparePage)

        self.re_translate_ui()

        self.goto_next_index(0, False)

    def re_translate_ui(self):
        self.next_button.setText(self.tr('Next'))
        self._page_list = [
            {"page": self.language_frame, "title": self.tr("Language")},
            {"page": self.wlan_frame, "title": self.tr("WLAN")},
            # {"page": self.usePreparePage, "title": self.tr("Use Prepare")},
            {"page": self.usePreparePage, "title": self.tr("Use Prepare")},
            # { "page": self.level_frame, "title": self.tr("Auto Bed Level")},
            # { "page": self.offset_frame, "title": self.tr("Probe Offsets")},
            # { "page": self.dial_frame, "title": self.tr("Dial Indicator")},
            # { "page": self.verify_frame, "title": self.tr("Print Verify")},
        ]

    @pyqtSlot()
    def on_next_button_clicked(self):
        if self.header.title.text() == self._page_list[-1]['title']:
            self.complete.emit()
        else:
            self.goto_next_index(self.current_index + 1)

    def goto_next_index(self, next_index: int, record=True):
        self.gotoPage(self._page_list[next_index]['page'], self._page_list[next_index]['title'], False)
        if self._page_list[next_index]['page'] == self.usePreparePage:
            self.next_button.setText(self.tr("Skip"))
        if record:
            self.current_index = next_index

    @pyqtSlot()
    def on_language_e_clicked(self):
        if self._printer.config.get_language() == 'Chinese':
            self.updateTranslator.emit("English")
            update_style(self.language_e, "checked")
            update_style(self.language_c, "unchecked")
            self.re_translate_ui()
            self.header.title.setText(self.tr("Language"))

    @pyqtSlot()
    def on_language_c_clicked(self):
        if self._printer.config.get_language() == 'English':
            self.updateTranslator.emit("Chinese")
            update_style(self.language_e, "unchecked")
            update_style(self.language_c, "checked")
            self.re_translate_ui()
            self.header.title.setText(self.tr("Language"))
