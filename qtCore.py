# QT CORE
# Change for PySide Or PyQt
import platform

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

load_length = 100
load_speed = 200
load_time = load_length * 60 / load_speed
unload_purge_length = 15
unload_purge_speed = load_speed
unload_length = 100
unload_speed = 1500
unload_time = unload_purge_length * 60 / unload_purge_speed + unload_length * 60 / unload_speed

filament_position = {'X': 190, 'Y': 20, 'Z': 120}

is_release = platform.system().lower() == 'linux'

enabled_verity = True


def update_style(widget: QWidget, name: str):
    widget.setObjectName(name)
    widget.setStyle(widget.style())


def rotate_image(label: QLabel, image: str, angle: int):
    angle += 45
    if angle >= 360:
        angle -= 360
    transform = QTransform().rotate(angle)
    rotated_image = QPixmap(image).transformed(transform, Qt.SmoothTransformation)
    label.setPixmap(rotated_image)

    return angle
