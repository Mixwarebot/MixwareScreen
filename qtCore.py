# QT CORE
# Change for PySide Or PyQt
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

checkedStyleSheet = "border-radius: 0; border-bottom: 3px solid #FF5A00; " \
                    "border-top-left-radius: 5px; border-top-right-radius: 5px;" \
                    "background: rgba(255, 100, 0, 0.1)"
uncheckedStyleSheet = "border-bottom: none; background: #FFFFFF"

load_length = 100
load_speed = 200
load_time = load_length * 60 / load_speed
unload_purge_length = 15
unload_purge_speed = load_speed
unload_length = 100
unload_speed = 1500
unload_time = unload_purge_length * 60 / unload_purge_speed + unload_length * 60 / unload_speed
