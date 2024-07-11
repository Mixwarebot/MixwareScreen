from qtCore import *
from ui.components.base.baseLine import BaseHLine
from ui.components.base.basePushButton import BasePushButton


class HelpScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("helpScrollArea")
        self.setStyleSheet("QScrollArea {border: none; background: transparent;}")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame {background: transparent;}")
        self.layout = QHBoxLayout(self.frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setWidget(self.frame)

    def add_widget(self, widget):
        self.layout.addWidget(widget)


class HelpPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self._parent = parent

        self.setObjectName("helpPage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame_layout = QHBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.helpScrollArea = HelpScrollArea()
        self.helpScrollArea.setFixedHeight(80)
        QScroller.grabGesture(self.helpScrollArea, QScroller.TouchGesture)
        self.help_1 = BasePushButton("组装前门")
        self.helpScrollArea.add_widget(self.help_1)
        self.help_2 = BasePushButton("调节XY补偿")
        self.helpScrollArea.add_widget(self.help_2)
        self.help_3 = BasePushButton("更换喷头组件")
        self.helpScrollArea.add_widget(self.help_3)
        self.frame_layout.addWidget(self.helpScrollArea)
        self.frame_layout.addWidget(BaseHLine())

        self.stackedLayout = QStackedWidget()
        self.help_1_frame = QFrame()
        self.help_1_label = QLabel(self.help_1_frame)
        self.help_1_label.setText("注意：亚克力易碎，请小心安装，防止跌落。")
        self.stackedLayout.addWidget(self.help_1_frame)
        self.frame_layout.addWidget(self.stackedLayout)
        self.layout.addWidget(self.frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        pass

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
