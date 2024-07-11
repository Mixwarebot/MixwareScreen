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


def update_style(w: QWidget, o: str):
    w.setObjectName(o)
    w.setStyle(w.style())
