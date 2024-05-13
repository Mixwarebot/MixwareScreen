import math
import numpy

from qtCore import *
from ui.pages.levelPages.bedMeshColor import BedMeshColor


class BedMeshGraph(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.color = BedMeshColor()
        self.setFixedHeight(400)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.title = QLabel()
        self.layout.addWidget(self.title)
        self.title.setObjectName("frame_title")
        self.title.setFixedHeight(40)
        self.body_frame = QFrame()
        self.body_frame.setObjectName("frameBox")
        self.body_frame.setFixedSize(360, 360)
        self.body_frame_layout = QGridLayout(self.body_frame)
        self.layout.addWidget(self.body_frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title.setText(self.tr("Auto-leveling Mesh Graph"))

    def get_opacity(self, model: list, num: int) -> int:
        # minimum = numpy.min(model)
        # maximum = numpy.max(model)
        # return (maximum - model[num]) / (maximum - minimum)

        _mean = numpy.mean(model)
        _min = numpy.min(model) if numpy.min(model) > _mean - 2.5 else _mean - 2.5
        _max = numpy.max(model) if numpy.min(model) < _mean + 2.5 else _mean + 2.5
        # _mean = (_max + _min) / 2
        # median = numpy.median(model)
        # mean = numpy.mean(model)
        return 50 + (model[num] - _mean) / (_max - _min) * 100

    def clear_bed_mesh(self):
        for i in range(self.body_frame_layout.count()):
            self.body_frame_layout.itemAt(i).widget().deleteLater()

    def show_bed_mesh(self, data: list):
        # clear layout
        self.clear_bed_mesh()
        # add widget
        if len(data):
            _grid_points = int(math.sqrt(len(data)))
            for x in range(_grid_points):
                for y in range(_grid_points):
                    label = QLabel(f"{data[x * _grid_points + y]:.2f}")
                    label.setAlignment(Qt.AlignCenter)
                    # opacity = self.get_opacity(data, x * _grid_points + y)
                    # label.setStyleSheet(f"background: rgba(255, 100, 0, {opacity});")
                    color = self.color.get_color_map(self.get_opacity(data, x * _grid_points + y))
                    label.setStyleSheet(f"background: rgb({color['r']}, {color['g']}, {color['b']});")
                    self.body_frame_layout.addWidget(label, x, y)
        else:
            tips = QLabel(self.tr("No data."))
            tips.setAlignment(Qt.AlignCenter)
            self.body_frame_layout.addWidget(tips)
