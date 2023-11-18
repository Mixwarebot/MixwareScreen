from qtCore import *

class PrintFileBar(QFrame):
    clicked = pyqtSignal(str)
    def __init__(self, file: QFileInfo):
        super().__init__()
        self.is_move = None
        self.setObjectName("frameBox")
        self.setFixedSize(360, 120)

        self._file = file
        if self._file.isDir():
            file_icon = QPixmap("resource/icon/dir.svg")
            file_size = 0
        else:
            file_icon = QPixmap("resource/icon/file.svg")
            file_size = self._file.size()
        file_time = file.fileTime(QFileDevice.FileModificationTime).toString("yyyy/MM/dd  hh:mm:ss")

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(file_icon))
        self.logo_label.setFixedSize(108, 108)

        self.name_label = QLabel()
        self.name_label.setText(self._file.fileName())
        self.name_label.setMaximumWidth(222)
        self.name_label.setWordWrap(True)

        self.time_label = QLabel()
        self.time_label.setText(file_time)
        self.time_label.setFixedHeight(22)
        self.time_label.setStyleSheet("font-size: 15px")
        if self._file.isDir():
            self.time_label.hide()

        self.size_label = QLabel()
        self.size_label.setFixedHeight(22)
        self.size_label.setStyleSheet("font-size: 15px")

        if not file_size:
            self.size_label.hide()
        else:
            size_h = ['B', 'KB', 'MB', 'GB']
            level = 0
            while file_size > 1024:
                file_size /= 1024
                level += 1
            if level:
                self.size_label.setText(f"{file_size:.2f}{size_h[level]}")
            else:
                self.size_label.setText(f"{file_size}{size_h[level]}")

        label_layout = QVBoxLayout()
        label_layout.setContentsMargins(5, 10, 15, 10)
        label_layout.setSpacing(0)
        label_layout.addWidget(self.name_label)
        label_layout.addWidget(self.time_label)
        label_layout.addWidget(self.size_label)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.logo_label)
        layout.addLayout(label_layout)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.clicked.emit(self._file.absoluteFilePath())

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.is_move = True

class PrintFilePage(QScrollArea):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("printFilePage")

        self.setStyleSheet("QScrollArea {border: none; background: transparent;}")
        self.setWidgetResizable(True)

        self.frame = QFrame()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.root_path = self._printer.config.get_folder_rootPath()
        self.current_path = self._printer.config.get_folder_rootPath()
        self.filters = ["*.gcode"]
        self.files = {}

        self.layout = QVBoxLayout(self.frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(10)
        self.setWidget(self.frame)

    def update_file(self, path: str):
        dir = QDir(path)
        dir.setFilter(QDir.Readable | QDir.Dirs | QDir.Files | QDir.NoDotAndDotDot | QDir.NoSymLinks)
        dir.setSorting(QDir.Time | QDir.DirsFirst)
        files = dir.entryInfoList()
        self.current_path = dir.absolutePath()

        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().deleteLater()

        for file in files:
            if file.isDir() or (file.isFile() and file.completeSuffix() == "gcode"):

                if file.isDir() and file.exists(f'{file.absoluteFilePath()}/firmware.cur'):
                    continue
                print_file_bar = PrintFileBar(file)
                print_file_bar.clicked.connect(self.on_printFileBar_clicked)
                self.layout.addWidget(print_file_bar)

    def on_printFileBar_clicked(self, path):
        file_info = QFileInfo(path)
        if file_info.isDir():
            self.update_file(path)
        else:
            self._parent.showShadowScreen()
            ret = self._parent.message.start("Mixware Screen", self.tr("Print {} ?").format(file_info.fileName()), buttons=QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self._printer.print_start(path)
            self._parent.closeShadowScreen()

    def showEvent(self, a0: QShowEvent) -> None:
        self.update_file(self.root_path)
