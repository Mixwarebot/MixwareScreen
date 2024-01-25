import base64
import os
import platform
import re
import logging

from typing import List, Optional, Dict, Any

from qtCore import *


def regex_find_ints(pattern: str, data: str) -> List[int]:
    pattern = pattern.replace(r"(%D)", r"([0-9]+)")
    matches = re.findall(pattern, data)
    if matches:
        # return the maximum height value found
        try:
            return [int(h) for h in matches]
        except Exception:
            pass
    return []


def parse_thumbnails(path: str) -> Optional[List[Dict[str, Any]]]:
    with open(path, 'r') as file:
        header_data = file.read()
        file.close()
    for data in [header_data]:
        thumb_matches: List[str] = re.findall(
            r"; thumbnail begin[;/\+=\w\s]+?; thumbnail end", data)
        if thumb_matches:
            break
    else:
        return None
    thumb_dir = os.path.join(os.path.dirname(path), ".thumbs")
    if not os.path.exists(thumb_dir):
        try:
            os.mkdir(thumb_dir)
        except Exception:
            print(f"Unable to create thumb dir: {thumb_dir}")
    thumb_base = os.path.splitext(os.path.basename(path))[0]
    parsed_matches: List[Dict[str, Any]] = []
    for match in thumb_matches:
        lines = re.split(r"\r?\n", match.replace('; ', ''))
        info = regex_find_ints(r"(%D)", lines[0])
        data = "".join(lines[1:-1])
        if len(info) != 3:
            logging.info(
                f"MetadataError: Error parsing thumbnail"
                f" header: {lines[0]}")
            continue
        if len(data) != info[2]:
            logging.info(
                f"MetadataError: Thumbnail Size Mismatch: "
                f"detected {info[2]}, actual {len(data)}")
            continue
        thumb_name = f"{thumb_base}.png"
        thumb_path = os.path.join(thumb_dir, thumb_name)
        abs_thumb_path = QFileInfo(thumb_path).absoluteFilePath()
        with open(thumb_path, "wb") as f:
            f.write(base64.b64decode(data.encode()))
        parsed_matches.append({
            'width': info[0], 'height': info[1],
            'size': os.path.getsize(thumb_path),
            'absolute_path': abs_thumb_path})
    return parsed_matches


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
            thumbnails_path = file.absolutePath() + '/.thumbs/' + file.completeBaseName() + '.png'
            if file.exists(thumbnails_path):
                file_icon = QPixmap(thumbnails_path)
            else:
                thumbnails = parse_thumbnails(file.absoluteFilePath())
                if thumbnails:
                    file_icon = QPixmap(thumbnails[0]['absolute_path'])
                else:
                    file_icon = QPixmap("resource/icon/file.svg")
            file_size = self._file.size()
        file_time = file.fileTime(QFileDevice.FileModificationTime).toString("yyyy/MM/dd  hh:mm:ss")

        if len(self._file.fileName()) > 20:
            file_name = list(self._file.fileName())
            file_name.insert(19, '\n')
            file_name = ''.join(file_name)
        else:
            file_name = self._file.fileName()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(0)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(96, 108)
        self.logo_label.setPixmap(file_icon.scaledToWidth(96))
        self.layout.addWidget(self.logo_label)

        self.label_layout = QVBoxLayout()
        self.label_layout.setContentsMargins(5, 5, 0, 5)
        self.label_layout.setSpacing(0)

        self.name_label = QLabel()
        self.name_label.setMaximumSize(239, 66)
        self.name_label.setWordWrap(True)
        self.name_label.setText(file_name)
        self.name_label.adjustSize()
        self.label_layout.addWidget(self.name_label)

        self.time_label = QLabel()
        self.time_label.setText(file_time)
        self.time_label.setFixedHeight(21)
        self.time_label.setObjectName("tips")
        if self._file.isDir():
            self.time_label.hide()
        self.label_layout.addWidget(self.time_label)

        self.size_label = QLabel()
        self.size_label.setFixedHeight(21)
        self.size_label.setObjectName("tips")
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
        self.label_layout.addWidget(self.size_label)
        self.layout.addLayout(self.label_layout)

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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.frame = QFrame()
        self.layout = QVBoxLayout(self.frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(10)
        self.setWidget(self.frame)

        self.root_path = ''
        self.current_path = ''
        self.filters = ["*.gcode"]
        self.files = {}

        self.set_usb_path()

    def showEvent(self, a0: QShowEvent) -> None:
        self.update_file(self.root_path)

    def set_local_path(self):
        self.root_path = QDir('resource/gcode').absolutePath()

    def set_usb_path(self):
        self.root_path = QDir('./').absolutePath()
        if platform.system().lower() == 'linux':
            self.root_path = QDir(self._printer.config.get_folder_rootPath()).absolutePath()

    def update_file(self, path: str):
        dir = QDir(path)
        dir.setFilter(QDir.Readable | QDir.Dirs | QDir.Files | QDir.NoDotAndDotDot | QDir.NoSymLinks)
        dir.setSorting(QDir.Time | QDir.DirsFirst)
        files = dir.entryInfoList()
        self.current_path = dir.absolutePath()

        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().deleteLater()

        for file in files:
            if file.isDir() or (file.isFile() and file.suffix() == "gcode"):

                if file.isDir():
                    if file.exists(f'{file.absoluteFilePath()}/firmware.cur'):
                        continue
                    if len(QDir(file.absoluteFilePath()).entryInfoList()) <= 2:
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
            if len(file_info.fileName()) > 20:
                file_name = list(file_info.fileName())
                file_name.insert(19, '\n')
                file_name = ''.join(file_name)
            else:
                file_name = file_info.fileName()

            image = f'{file_info.absolutePath()}/.thumbs/{file_info.completeBaseName()}.png'
            if not os.path.isfile(image):
                image = ''

            ret = self._parent.message.start("Mixware Screen", self.tr("Print {} ?").format(file_name), image,
                                             buttons=QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self._printer.print_start(path)
            self._parent.closeShadowScreen()
