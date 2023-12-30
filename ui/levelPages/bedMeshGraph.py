import math
import numpy

from qtCore import *


class BedMeshGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title.setText(self.tr("Auto-leveling Mesh Graph"))

    def get_opacity(self, model: list, num: int):
        minimum = numpy.min(model)
        maximum = numpy.max(model)
        return (maximum - model[num]) / (maximum - minimum)

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
                    opacity = self.get_opacity(data, x * _grid_points + y)
                    label.setStyleSheet(f"background: rgba(255, 100, 0, {opacity});")
                    self.body_frame_layout.addWidget(label, x, y)
        else:
            tips = QLabel(self.tr("No data."))
            tips.setAlignment(Qt.AlignCenter)
            self.body_frame_layout.addWidget(tips)
