import math

import numpy

from qtCore import *


class BedMeshGraph(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(400)

        self.plan_frame_title = QLabel()
        self.plan_body_frame = QFrame()
        self.plan_body_frame_layout = QGridLayout(self.plan_body_frame)

        self.initForm()
        self.initLayout()

    def initForm(self):
        self.plan_frame_title.setFixedHeight(40)
        self.plan_frame_title.setObjectName("frame_title")

        self.plan_body_frame.setObjectName("frameBox")
        self.plan_body_frame.setFixedSize(360, 360)

        self.plan_frame_title.setText(self.tr("Auto-level Mesh Graph"))

    def initLayout(self):
        plan_frame_layout = QVBoxLayout(self)
        plan_frame_layout.setContentsMargins(0, 0, 0, 0)
        plan_frame_layout.setSpacing(0)
        plan_frame_layout.addWidget(self.plan_frame_title)
        plan_frame_layout.addWidget(self.plan_body_frame)

    def get_opacity(self, model: list, num: int):
        minimum = numpy.min(model)
        maximum = numpy.max(model)
        return (maximum - model[num]) / (maximum - minimum)

    def clear_bed_mesh(self):
        for i in range(self.plan_body_frame_layout.count()):
            self.plan_body_frame_layout.itemAt(i).widget().deleteLater()

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
                    self.plan_body_frame_layout.addWidget(label, x, y)
        else:
            tips = QLabel(self.tr("No data."))
            tips.setAlignment(Qt.AlignCenter)
            self.plan_body_frame_layout.addWidget(tips)