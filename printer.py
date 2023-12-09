# This Python file uses the following encoding: utf-8
import functools
import logging
import platform
import re
import sys
from pathlib import Path
from time import time
from queue import Queue
from threading import Thread, Event
from typing import Union, cast

import netifaces
import serial
import serial.tools.list_ports

from qtCore import *
from serial import SerialException, SerialTimeoutException

from config import MixwareScreenConfig


def scan_serial_list():
    serial_list_name = []
    serial_list = serial.tools.list_ports.comports()
    if serial_list:
        for serial_port in serial_list:
            serial_list_name.append(serial_port.device)
            logging.debug(F"Found serial port: {serial_port.device}")
    return serial_list_name


class MixwareScreenPrinter(QObject):
    config = None
    _version = None

    updatePrinterStatus = pyqtSignal(int)
    """
    0: printer disconnected; 
    1: printer connected; 
    2: printer printing; 
    3: printer print finished;
    4: auto-leveling finished;
    5: filament finished;
    """
    updatePrinterInformation = pyqtSignal()
    updatePrinterMessage = pyqtSignal(str, int)
    """
    message: str
    level: int
        0: info
        1: warning
        2: error
    """

    def __init__(self):
        super(MixwareScreenPrinter, self).__init__()
        self.dial_indicator = {'left': 0.0, 'right': 0.0}
        self.print_file = ""
        self.serial = None
        self.serial_data = ""
        self.re_data = ""

        self._version = "v1.0.0"
        self._device_name = "Unknown"
        self._device_version = "Unknown"
        self.information = {}
        self.printing_information = {}
        self._gcode = []
        self._gcode_line = ""

        self.connected = False
        self.connecting = False
        self._printer_busy = False
        self._is_printing = False
        self._is_print_verify = False
        self._is_paused = False
        self.leveling_working = 0
        self.filament_working = 0
        self.connect_timer = QTimer()
        self.connect_timer.timeout.connect(self.onTimerTriggered)
        self.connect_timer.start(1000)
        self.connect_check_timer = QTimer()
        self.connect_check_timer.timeout.connect(self.connect_check)

        self._last_temperature_request = None
        self._firmware_idle_count = 0
        self._serial_error_count = 0
        self._timeout = 1
        self._gcode_position = 0
        self._update_thread = Thread(target=self._update, daemon=True, name="USBPrinterUpdate")

        self._command_queue = Queue()
        self._command_received = Event()
        self._command_received.set()

        self.config = None
        self.repository = None

        self.reset_information()

    def reset_information(self):
        self.information = {
            'thermal': {
                'extruder': 'left',
                'protection': True,
                'left': {'temperature': 0.0, 'target': 0.0, 'power': 0.0},
                'right': {'temperature': 0.0, 'target': 0.0, 'power': 0.0},
                'bed': {'temperature': 0.0, 'target': 0.0, 'power': 0.0},
                'chamber': {'temperature': 0.0, 'target': 0.0, 'power': 0.0},
                'PID': {'P': 0.0, 'I': 0.0, 'D': 0.0}
            },
            'fan': {
                'left': {'speed': 0.0},
                'right': {'speed': 0.0},
                'chamber': {'speed': 0.0},
                'leftCool': {'speed': 0.0},
                'rightCool': {'speed': 0.0},
                'exhaust': {'speed': 0.0}
            },
            'led': {'light': 0.0},
            'home': {'X': False, 'Y': False, 'Z': False},
            'endstop': {'X': False, 'X2': False, 'Y': False, 'Z': False, 'Z2': False, 'probe': False},
            'bedMesh': [],
            'probe': {
                'offset': {
                    'left': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
                    'right': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
                }
            },
            'motor': {
                'position': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'E': 0.0},
                'stepPerUnit': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'E': 0.0},
                'maxFeedRate': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'E': 0.0},
                'maxAcceleration': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'E': 0.0},
                'jerk': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'E': 0.0},
                'acceleration': 0.0,
                'accelerationRetract': 0.0,
                'accelerationTravel': 0.0,
                'drivers': {
                    'connected': {'X': False, 'X2': False, 'Y': False, 'Z': False, 'Z2': False, 'E': False,
                                  'E1': False},
                    'current': {'X': 0.0, 'X2': 0.0, 'Y': 0.0, 'Z': 0.0, 'Z2': 0.0, 'E': 0.0, 'E1': 0.0},
                    'microSteps': {'X': 0.0, 'X2': 0.0, 'Y': 0.0, 'Z': 0.0, 'Z2': 0.0, 'E': 0.0, 'E1': 0.0},
                }
            },
            'inputShaping': {
                'X': {'frequency': 0.0, 'damping': 0.0},
                'Y': {'frequency': 0.0, 'damping': 0.0}
            },
            'printMode': 'Normal',
            'feedRate': 100,
            'flow': {'left': 100, 'right': 100},
            'linearAdvance': 0.0,
            'runOut': {'enabled': False, 'distance': 0}
        }

    def serial_close(self):
        if self.serial is not None:
            logging.debug(F"Close serial {self.serial.name}.")
            self.serial.close()
            self.serial = None

        # Re-create the thread, so it can be started again later.
        self._update_thread = Thread(target=self._update, daemon=True, name="USBPrinterUpdate")
        self.connected = False

    @pyqtSlot()
    def connect_serial(self):
        self.serial_close()
        serial_list = scan_serial_list()
        if len(serial_list):
            try:
                self.serial = serial.Serial(serial_list[0], 115200, timeout=self._timeout, writeTimeout=self._timeout)
            except SerialException:
                logging.warning("An exception occurred while trying to create serial connection.")
                return
            except OSError as e:
                logging.warning(
                    "The serial device is suddenly unavailable while trying to create a serial connection: "
                    "{err}".format(err=str(e)))
                return

            if self.serial is not None:
                logging.debug(F"Serial connected successfully.")
                self.reset_information()
                while not self._command_queue.empty():
                    self._command_queue.get()
                self._device_name = "Unknown"
                self._device_version = "Unknown"
                self.print_file = ""
                self._printer_busy = False
                self.connected = False
                self.connecting = True
                self._is_printing = False
                self._is_print_verify = False
                self._update_thread.start()
                self.connect_check_timer.start(500)
                QTimer.singleShot(5000, self.connect_check_timeout)

    def _update(self):
        pull_thermal = True
        while self.serial is not None and self.connected or self.connecting:
            try:
                self.serial_data = str(self.serial.readline(), "ascii")
            except Exception as e:
                self._serial_error_count += 1
                logging.warning(F"Serial port read exception.@{self._serial_error_count}")
                if self._serial_error_count > 99:
                    # ClearCommError failed (PermissionError(13, '设备不识别此命令。', None, 22))
                    if "ClearCommError failed" in str(e):
                        self.updatePrinterMessage.emit("The printer disconnected abnormally.", 2)
                        self.serial_error()
                    # device reports readiness to read but returned no data (device disconnected or multiple access on port?)
                    elif "device reports readiness to read but returned no data" in str(e):
                        self.updatePrinterMessage.emit("The printer disconnected abnormally.", 2)
                        self.serial_error()
                    else:
                        logging.error(F"Serial error.@{e}")
                    # self.serial_error()
                continue

            if 'echo:' in self.serial_data and 'Failed' in self.serial_data:
                self.updatePrinterMessage.emit(
                    self.serial_data[self.serial_data.find('echo:') + 5:self.serial_data.rfind('\n')], 2)
                logging.error(F"Printer error: {self.serial_data}")
                continue

            self._serial_error_count = 0
            if self.connecting and not self.connected:
                self.set_level_state()
                self.set_filament_state()
                self._printer_busy = False
                self.print_file = ""
                self.connecting = False
                self.connected = True
                self._gcode_position = 0
                logging.debug(F"Printer connected successfully.Get printer information.")
                # self.write_gcode_command('M605 S1\nM115\nM503\nM154 S2\nM155 S2 R')
                self.write_gcode_command('M605 S1\nM115\nM503')

            if self._last_temperature_request is None or time() > self._last_temperature_request + self._timeout:
                # Timeout, or no request has been sent at all.
                if not self._printer_busy:  # Don't flood the printer with temperature requests while it is busy
                    # self.sendCommand("M105")
                    if pull_thermal:
                        self.sendCommand("M105")
                    else:
                        self.sendCommand("M114")
                    pull_thermal ^= True
                    self._last_temperature_request = time()

            if "FIRMWARE_NAME:" in self.serial_data:
                self._setPrinterInformation(self.serial_data)
                self.updatePrinterStatus.emit(self.connected)

            if "Active Extruder" in self.serial_data:  # Active extruder.
                self.re_data = re.findall("Active Extruder: (\\d+)", self.serial_data)
                if self.re_data:
                    if int(self.re_data[0]) == 0:
                        self.information['thermal']['extruder'] = 'left'
                    elif int(self.re_data[0]) == 1:
                        self.information['thermal']['extruder'] = 'right'
                    logging.debug(F"Active Extruder: {self.information['thermal']['extruder']} extruder.")
                    self.re_data.clear()
                    self.updatePrinterInformation.emit()
            elif re.search("[B|C|T\\d*]: ?\\d+\\.?\\d*", self.serial_data):
                self.re_data = re.findall("T(\\d*): ?(-?\\d+\\.?\\d*)\\s*/?(\\d+\\.?\\d*)?", self.serial_data)
                if len(self.re_data) == 1:
                    if self.re_data[0]:
                        if self.re_data[0][1]:
                            self.information['thermal']['left']['temperature'] = float(self.re_data[0][1])
                            if self.information['thermal']['left']['temperature'] >= 60:
                                self.information['fan']['leftCool']['speed'] = 1.0
                            else:
                                self.information['fan']['leftCool']['speed'] = 0.0
                        if self.re_data[0][2]:
                            self.information['thermal']['left']['target'] = float(self.re_data[0][2])
                    self.re_data.clear()
                elif len(self.re_data) == 3:
                    if self.re_data[1]:
                        if self.re_data[1][1]:
                            self.information['thermal']['left']['temperature'] = float(self.re_data[1][1])
                            if self.information['thermal']['left']['temperature'] >= 60:
                                self.information['fan']['leftCool']['speed'] = 1.0
                            else:
                                self.information['fan']['leftCool']['speed'] = 0.0
                        if self.re_data[1][2]:
                            self.information['thermal']['left']['target'] = float(self.re_data[1][2])
                    if self.re_data[2]:
                        if self.re_data[2][1]:
                            self.information['thermal']['right']['temperature'] = float(self.re_data[2][1])
                            if self.information['thermal']['right']['temperature'] >= 60:
                                self.information['fan']['rightCool']['speed'] = 1.0
                            else:
                                self.information['fan']['rightCool']['speed'] = 0.0
                        if self.re_data[2][2]:
                            self.information['thermal']['right']['target'] = float(self.re_data[2][2])
                    self.re_data.clear()
                self.re_data = re.findall("B: ?(-?\\d+\\.?\\d*)\\s*/?(\\d+\\.?\\d*)?", self.serial_data)
                if self.re_data and self.re_data[0]:
                    if self.re_data[0][0]:
                        self.information['thermal']['bed']['temperature'] = float(self.re_data[0][0])
                    if self.re_data[0][1]:
                        self.information['thermal']['bed']['target'] = float(self.re_data[0][1])
                    self.re_data.clear()
                self.re_data = re.findall("C: ?(-?\\d+\\.?\\d*)\\s*/?(\\d+\\.?\\d*)?", self.serial_data)
                if self.re_data and self.re_data[0]:
                    if self.re_data[0][0]:
                        self.information['thermal']['chamber']['temperature'] = float(self.re_data[0][0])
                        if self.information['thermal']['chamber']['temperature'] >= 50:
                            self.information['fan']['chamber']['speed'] = 1.0
                        else:
                            self.information['fan']['chamber']['speed'] = 0.0
                    if self.re_data[0][1]:
                        self.information['thermal']['chamber']['target'] = float(self.re_data[0][1])
                    self.re_data.clear()
                # left_power = re.findall("@0: ?(\d+)?", data)
                # if left_power:
                #     self.information['thermal']['left']['power'] = float(left_power[0])
                # right_power = re.findall("@1: ?(\d+)?", data)
                # if right_power:
                #     self.information['thermal']['right']['power'] = float(right_power[0])
                #
                # bed_power = re.findall("B@: ?(\d+)?", data)
                # if bed_power:
                #     self.information['thermal']['bed']['power'] = float(bed_power[0])
                # chamber_power = re.findall("C@: ?(\d+)?", data)
                # if chamber_power:
                #     self.information['thermal']['chamber']['power'] = float(chamber_power[0])
                self.updatePrinterInformation.emit()
            elif re.search("[X|Y|Z|E]:-?\\d+\\.?\\d*", self.serial_data) and 'Count' in self.serial_data:
                self.re_data = re.findall("[X|Y|Z|E]:(-?\\d+\\.?\\d*)", self.serial_data)
                if self.re_data:
                    self.information['motor']['position']['X'] = float(self.re_data[0])
                    self.information['motor']['position']['Y'] = float(self.re_data[1])
                    self.information['motor']['position']['Z'] = float(self.re_data[2])
                    self.information['motor']['position']['E'] = float(self.re_data[3])
                    self.re_data.clear()
                    self.updatePrinterInformation.emit()
            elif re.search("FR:\\d*%", self.serial_data):
                self.re_data = re.findall("FR:(\\d*)%", self.serial_data)
                if self.re_data:
                    logging.debug(F"Update printer feed rate(M220): {self.re_data[0]}")
                    self.information['feedrate'] = int(self.re_data[0])
                    self.re_data.clear()
            elif re.search("E\\d* Flow: \\d*%", self.serial_data):
                self.re_data = re.findall("E(\\d) Flow: (\\d*)%", self.serial_data)
                if self.re_data:
                    if int(self.re_data[0][0]) == 0:
                        self.information['flow']['left'] = int(self.re_data[0][1])
                        logging.debug(F"Update printer left extruder flow rate(M221): {self.re_data[0][1]}")
                    if int(self.re_data[0][0]) == 1:
                        logging.debug(F"Update printer right extruder flow rate(M221): {self.re_data[0][1]}")
                        self.information['flow']['right'] = int(self.re_data[0][1])
                    self.re_data.clear()
            elif re.search("M218 T1", self.serial_data):
                self.re_data = re.findall("M218 T1 X(-?\\d+\\.?\\d*) Y(-?\\d+\\.?\\d*) Z(-?\\d+\\.?\\d*)",
                                          self.serial_data)
                if self.re_data:
                    logging.debug(F"Update printer right probe offset(M218): {self.re_data}")
                    self.information['probe']['offset']['right']['X'] = float(self.re_data[0][0])
                    self.information['probe']['offset']['right']['Y'] = float(self.re_data[0][1])
                    self.information['probe']['offset']['right']['Z'] = float(self.re_data[0][2])
                    self.re_data.clear()
            elif re.search("M851", self.serial_data):
                self.re_data = re.findall("M851 X(-?\\d+\\.?\\d*) Y(-?\\d+\\.?\\d*) Z(-?\\d+\\.?\\d*)",
                                          self.serial_data)
                if self.re_data:
                    logging.debug(F"Update printer left probe offset(M851): {self.re_data}")
                    self.information['probe']['offset']['left']['X'] = float(self.re_data[0][0])
                    self.information['probe']['offset']['left']['Y'] = float(self.re_data[0][1])
                    self.information['probe']['offset']['left']['Z'] = float(self.re_data[0][2])
                    self.re_data.clear()
            elif re.search("M106", self.serial_data):  # Fan & LED speed
                self.re_data = re.findall("M106 P\\d* S(\\d*) P\\d* S(\\d*) P\\d* S(\\d*) P\\d* S(\\d*)",
                                          self.serial_data)
                if self.re_data:
                    logging.debug(F"Update fan status(M106): {self.re_data}")
                    self.information['fan']['left']['speed'] = int(self.re_data[0][0]) / 255
                    self.information['fan']['right']['speed'] = int(self.re_data[0][1]) / 255
                    self.information['fan']['exhaust']['speed'] = int(self.re_data[0][2]) / 255
                    self.re_data.clear()
            elif re.search("Case light", self.serial_data):  # LED light
                self.re_data = re.findall("Case light: (\\d*)", self.serial_data)
                if self.re_data:
                    if not self.re_data[0]:
                        self.information['led']['light'] = 0
                    else:
                        self.information['led']['light'] = int(self.re_data[0]) / 255
                    self.re_data.clear()
                    logging.debug(F"Update led status(M355): {self.information['led']['light']}")
            else:
                if re.search("M92", self.serial_data):
                    self.re_data = re.findall("M92 X(\\d+\\.?\\d*) Y(\\d+\\.?\\d*) Z(\\d+\\.?\\d*) E(\\d+\\.?\\d*)",
                                              self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer steps per unit(M92): {self.re_data}")
                        self.information['motor']['stepPerUnit']['X'] = float(self.re_data[0][0])
                        self.information['motor']['stepPerUnit']['Y'] = float(self.re_data[0][1])
                        self.information['motor']['stepPerUnit']['Z'] = float(self.re_data[0][2])
                        self.information['motor']['stepPerUnit']['E'] = float(self.re_data[0][3])
                        self.re_data.clear()
                elif re.search("M201", self.serial_data):
                    self.re_data = re.findall("M201 X(\\d+\\.?\\d*) Y(\\d+\\.?\\d*) Z(\\d+\\.?\\d*) E(\\d+\\.?\\d*)",
                                              self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer max acceleration(M201): {self.re_data}")
                        self.information['motor']['maxAcceleration']['X'] = float(self.re_data[0][0])
                        self.information['motor']['maxAcceleration']['Y'] = float(self.re_data[0][1])
                        self.information['motor']['maxAcceleration']['Z'] = float(self.re_data[0][2])
                        self.information['motor']['maxAcceleration']['E'] = float(self.re_data[0][3])
                elif re.search("M203", self.serial_data):
                    self.re_data = re.findall("M203 X(\\d+\\.?\\d*) Y(\\d+\\.?\\d*) Z(\\d+\\.?\\d*) E(\\d+\\.?\\d*)",
                                              self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer max feed rate(M203): {self.re_data}")
                        self.information['motor']['maxFeedRate']['X'] = float(self.re_data[0][0])
                        self.information['motor']['maxFeedRate']['Y'] = float(self.re_data[0][1])
                        self.information['motor']['maxFeedRate']['Z'] = float(self.re_data[0][2])
                        self.information['motor']['maxFeedRate']['E'] = float(self.re_data[0][3])
                        self.re_data.clear()
                elif re.search("M204", self.serial_data):
                    self.re_data = re.findall("M204 P(\\d+\\.?\\d*) R(\\d+\\.?\\d*) T(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer acceleration(M204): {self.re_data}")
                        self.information['motor']['acceleration'] = float(self.re_data[0][0])
                        self.information['motor']['accelerationRetract'] = float(self.re_data[0][1])
                        self.information['motor']['accelerationTravel'] = float(self.re_data[0][2])
                        self.re_data.clear()
                elif re.search("M205", self.serial_data):
                    self.re_data = re.findall(
                        "M205 B(\\d+\\.?\\d*) S(\\d+\\.?\\d*) T(\\d+\\.?\\d*) "
                        "X(\\d+\\.?\\d*) Y(\\d+\\.?\\d*) Z(\\d+\\.?\\d*) E(\\d+\\.?\\d*)",
                        self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer jerk(M205): {self.re_data}")
                        self.information['motor']['jerk']['X'] = float(self.re_data[0][3])
                        self.information['motor']['jerk']['Y'] = float(self.re_data[0][4])
                        self.information['motor']['jerk']['Z'] = float(self.re_data[0][5])
                        self.information['motor']['jerk']['E'] = float(self.re_data[0][6])
                        self.re_data.clear()
                elif re.search("M301", self.serial_data):
                    self.re_data = re.findall("M301 P(\\d+\\.?\\d*) I(\\d+\\.?\\d*) D(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        self.information['thermal']['PID']['P'] = float(self.re_data[0][0])
                        self.information['thermal']['PID']['I'] = float(self.re_data[0][1])
                        self.information['thermal']['PID']['D'] = float(self.re_data[0][2])
                        self.re_data.clear()
                # if re.search("M420 S\d*:", data):
                #     self.re_data = re.findall("M420 S(\d*)", data)
                #     if self.re_data:
                #         print(self.re_data)
                elif re.search("M593 X", self.serial_data):  # Input Shaping
                    self.re_data = re.findall("M593 X F(\\d+\\.?\\d*) D(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer input shaping x-axis(M593): {self.re_data}")
                        self.information['inputShaping']['X']['frequency'] = float(self.re_data[0][0])
                        self.information['inputShaping']['X']['damping'] = float(self.re_data[0][1])
                        self.re_data.clear()
                elif re.search("M593 Y", self.serial_data):
                    self.re_data = re.findall("M593 Y F(\\d+\\.?\\d*) D(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer input shaping y-axis(M593): {self.re_data}")
                        self.information['inputShaping']['Y']['frequency'] = float(self.re_data[0][0])
                        self.information['inputShaping']['Y']['damping'] = float(self.re_data[0][1])
                        self.re_data.clear()
                elif re.search("M900", self.serial_data):  # Linear Advance
                    self.re_data = re.findall("M900 K(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer linear advance k(M900): {self.re_data}")
                        self.information['linearAdvance'] = float(self.re_data[0])
                        self.re_data.clear()
                elif re.search("Advance K=", self.serial_data):  # Linear Advance
                    self.re_data = re.findall("Advance K=(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer linear advance k(M900): {self.re_data}")
                        self.information['linearAdvance'] = float(self.re_data[0])
                        self.re_data.clear()
                elif re.search("M906", self.serial_data):  # TMC Current.
                    self.re_data = re.findall("M906 X(\\d*) Y(\\d*) Z(\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer TMC drivers current(M906): {self.re_data}")
                        self.information['motor']['drivers']['current']['X'] = int(self.re_data[0][0])
                        self.information['motor']['drivers']['current']['Y'] = int(self.re_data[0][1])
                        self.information['motor']['drivers']['current']['Z'] = int(self.re_data[0][2])
                        self.re_data.clear()
                    self.re_data = re.findall("M906 I1 X(\\d*) Z(\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer TMC drivers current(M906): {self.re_data}")
                        self.information['motor']['drivers']['current']['X2'] = int(self.re_data[0][0])
                        self.information['motor']['drivers']['current']['Z2'] = int(self.re_data[0][1])
                        self.re_data.clear()
                    self.re_data = re.findall("M906 T0 E(\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer TMC drivers current(M906): {self.re_data}")
                        self.information['motor']['drivers']['current']['E'] = int(self.re_data[0])
                        self.re_data.clear()
                    self.re_data = re.findall("M906 T1 E(\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer TMC drivers current(M906): {self.re_data}")
                        self.information['motor']['drivers']['current']['E1'] = int(self.re_data[0])
                        self.re_data.clear()
                elif re.search("driver current: \\d*", self.serial_data):
                    self.re_data = re.findall("(\\w?\\d*) driver current: (\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer TMC drivers current(M906): {self.re_data}")
                        for dat in self.re_data:
                            if dat[0]:
                                self.information['motor']['drivers']['current'][dat[0]] = int(dat[1])
                        self.re_data.clear()
                elif re.search("G29 W", self.serial_data):  # Auto-leveling mesh value.
                    self.re_data = re.findall("G29 W I\\d* J\\d* Z(-?\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update printer auto-leveling data(G29): {self.re_data}")
                        self.information['bedMesh'].append(float(self.re_data[0]))
                        self.re_data.clear()
                elif re.search("D28", self.serial_data):  # Home status.
                    self.re_data = re.findall("D28 X(\\d*) Y(\\d*) Z(\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update home status(D28): {self.re_data}")
                        self.information['home']['X'] = bool(self.re_data[0][0])
                        self.information['home']['Y'] = bool(self.re_data[0][1])
                        self.information['home']['Z'] = bool(self.re_data[0][2])
                        self.re_data.clear()
                elif re.search("M412", self.serial_data):  # Run out status.
                    self.re_data = re.findall("M412 S(\\d*) D(\\d+\\.?\\d*)", self.serial_data)
                    if self.re_data:
                        logging.debug(F"Update run out status(M412): {self.re_data}")
                        self.information['runOut']['enabled'] = bool(self.re_data[0][0])
                        self.information['runOut']['distance'] = float(self.re_data[0][1])
                elif re.search("D412", self.serial_data):  # Run out status.
                    logging.debug(F"M412: {self.serial_data}")
                    self.re_data = re.findall("D412 B(\\d*) S(\\d*) T(\\d*)", self.serial_data)
                    logging.debug(F"M412: {self.re_data}")
                    if self.re_data:
                        if bool(self.re_data[0][0]) and self._is_printing and not self._is_paused:
                            self.print_pause()


            if self.serial_data == "":
                # An empty line means that the firmware is idle
                # Multiple empty lines probably means that the firmware and Screen are waiting
                # for each other due to a missed "ok", so we keep track of empty lines
                self._firmware_idle_count += 1
            else:
                self._firmware_idle_count = 0

            if self.serial_data.startswith("ok") or self._firmware_idle_count > 1:
                self._printer_busy = False

                if self.leveling_working:
                    self.leveling_working -= 1
                    if self.leveling_working == 0:
                        self.updatePrinterStatus.emit(4)
                if self.filament_working:
                    self.filament_working += 1
                    if self.filament_working > 5:
                        self.set_filament_state()
                        self.updatePrinterStatus.emit(5)

                self._command_received.set()
                if not self._command_queue.empty():
                    self._sendCommand(self._command_queue.get())
                elif self._is_printing:
                    if self._is_paused:
                        pass  # Nothing to do!
                    else:
                        self._sendNextGcodeLine()

                elif self._is_print_verify:
                    self._sendNextGcodeLine()

            if self.serial_data.startswith("echo:busy:"):
                self._printer_busy = True

            if self._is_printing or self._is_print_verify:
                if self.serial_data.startswith('!!'):
                    logging.error("Printer signals fatal error. Cancelling print. {}".format(self.serial_data))
                    self.print_stop()
                elif self.serial_data.lower().startswith("resend") or self.serial_data.startswith("rs"):
                    # A resend can be requested either by Resend, resend or rs.
                    try:
                        self._gcode_position = int(
                            self.serial_data.replace("N:", " ").replace("N", " ").replace(":", " ").split()[-1])
                    except:
                        if self.serial_data.startswith("rs"):
                            # In some cases of the RS command it needs to be handled differently.
                            self._gcode_position = int(self.serial_data.split()[1])

    @pyqtSlot(str)
    def write_gcode_commands(self, command):
        if '\n' not in command[-1]:
            command += '\n'
        pos_left = 0
        for pos, char in enumerate(command):
            if char == '\n':
                self.sendCommand(command[pos_left:pos + 1])
                pos_left = pos + 1

    @pyqtSlot(str)
    def write_gcode_command(self, command):
        if '\n' not in command[-1]:
            command += '\n'
        self._sendCommand(command)

    def sendCommand(self, command: Union[str, bytes]):
        """Send a command to printer."""
        if not self._command_received.is_set():
            self._command_queue.put(command)
        else:
            self._sendCommand(command)

    def _sendCommand(self, command: Union[str, bytes]):
        if self.serial is None or not self.connected:
            return
        new_command = cast(bytes, command) if type(command) is bytes else cast(str, command).encode()  # type: bytes
        if not new_command.endswith(b"\n"):
            new_command += b"\n"
        try:
            self._command_received.clear()
            self.serial.write(new_command)
            if b'G29' in new_command:
                logging.info("Start Auto-leveling(G29).")
                self.set_level_state(new_command.count(b"\n"))
            elif b'M502' in new_command:
                self.information['bedMesh'] = []
            elif b'M605' in new_command:
                if b'S1' in new_command:
                    logging.info("Dual x-carriage movement mode changed to DXC_AUTO_PARK_MODE")
                    self.information['printMode'] = 'Normal'
                elif b'S2' in new_command:
                    logging.info("Dual x-carriage movement mode changed to DXC_DUPLICATION_MODE")
                    self.information['printMode'] = 'Duplication'
                elif b'S3' in new_command:
                    logging.info("Dual x-carriage movement mode changed to DXC_MIRRORED_MODE")
                    self.information['printMode'] = 'Mirrored'
                else:
                    logging.warning("Dual x-carriage movement mode setting error.")
        except SerialTimeoutException:
            logging.warning("Timeout when sending command to printer via USB.")
            self._command_received.set()
        except SerialException:
            logging.warning("An unexpected exception occurred while writing to the serial.")
            self.serial_error()

    def _sendNextGcodeLine(self):
        """
        Send the next line of g-code, at the current `_gcode_position`, via a
        serial port to the printer.
        If the print is done, this sets `_is_printing` to `False` as well.
        """
        try:
            self._gcode_line = self._gcode[self._gcode_position]
        except IndexError:  # End of print, or print got cancelled.
            if self._gcode_position >= len(self._gcode):
                if self._is_printing:
                    logging.debug(F"Printing finished.")
                    self._is_printing = False
                    self.updatePrinterStatus.emit(3)
                    self._sendCommand('M77')
                    self._sendCommand("M500")
                elif self._is_print_verify:
                    logging.debug(F"Print verify finished.")
                    self._is_print_verify = False
            return

        if ";" in self._gcode_line:
            self._gcode_line = self._gcode_line[:self._gcode_line.find(";")]
        self._gcode_line = self._gcode_line.strip()

        # Don't send empty lines. But we do have to send something, so send M105 instead.
        # Don't send the M0 or M1 to the machine, as M0 and M1 are handled as an LCD menu pause.
        if self._gcode_line == "" or self._gcode_line == "M0" or self._gcode_line == "M1":
            self._gcode_line = "M105"

        checksum = functools.reduce(lambda x, y: x ^ y, map(ord, "N%d%s" % (self._gcode_position, self._gcode_line)))
        self._sendCommand("N%d%s*%d" % (self._gcode_position, self._gcode_line, checksum))
        self._gcode_position += 1

    def serial_error(self):
        if self.is_connected():
            self.serial_close()
            self.connected = False
            self.updatePrinterStatus.emit(self.connected)
            logging.error(F"Serial error, printer disconnected.")

    def _setPrinterInformation(self, name):
        new_version = re.findall(r"FIRMWARE_NAME:(.*) \(", str(name))

        if new_version:
            self._device_version = str(new_version[0])
            logging.info("USB output device Firmware version: %s", self._device_version)
        else:
            self._device_version = "Unknown"
            logging.info("Unknown USB output device Firmware version: %s", str(name))

        new_name = re.findall(r"MACHINE_TYPE:(.*) E", str(name))
        if new_name:
            self._device_name = str(new_name[0])
            logging.info("USB output device name: %s", self._device_name)
        else:
            self._device_name = "Unknown"
            logging.info("Unknown USB output device name: %s", str(name))

    @pyqtSlot(result=str)
    def deviceVersion(self):
        return self._device_version

    @pyqtSlot(result=str)
    def deviceName(self):
        return self._device_name

    @pyqtSlot(result=bool)
    def is_connected(self):
        return self.serial is not None and self.connected and not self.connecting

    @pyqtSlot(result=bool)
    def is_connecting(self):
        return self.serial is not None and not self.connected and self.connecting

    @pyqtSlot(result=bool)
    def is_busy(self):
        return self._printer_busy

    @pyqtSlot(result=QVariant)
    def get_information(self):
        return self.information

    @pyqtSlot(result=int)
    def get_target(self, heater: str):
        return int(self.information['thermal'][heater]['target'])

    @pyqtSlot(result=int)
    def get_temperature(self, heater: str):
        return int(self.information['thermal'][heater]['temperature'])

    @pyqtSlot(result=str)
    def get_thermal(self, heater: str):
        _temp = ""
        if heater in ['left', 'right', 'bed', 'chamber']:
            temp = self.get_temperature(heater)
            target = self.get_target(heater)
            power = int(self.information['thermal'][heater]['power'])
            _temp = str(temp)
            if target != 0:
                _temp += ' / ' + str(target)
            _temp += '°C'
            if False and power != 0:
                _temp += ' ' + str(power)

        return _temp

    @pyqtSlot(str, int)
    def set_thermal(self, heater, target):
        """
        Gcode: M104 - Set extruder target temp.
        Gcode: M140 - Set bed target temp.S < temp >
        Gcode: M141 - Set heated chamber target temp.S < temp > (Requires a chamber heater)
        :param heater: 'left', 'right', 'bed', 'chamber'
        :param target: target temperature (int)
        """
        command = ""
        if 'left' in heater:
            command = "M104 T0"
        elif 'right' in heater:
            command += "M104 T1"
        elif 'bed' in heater:
            command = "M140"
        elif 'chamber' in heater:
            command = "M141"
        if command:
            command += " S" + str(target) + "\nM105"
            self.write_gcode_commands(command)

    @pyqtSlot(result=str)
    def get_extruder(self):
        return self.information['thermal']['extruder']

    @pyqtSlot(str)
    def set_extruder(self, extruder: str):
        if extruder == "left":
            self.write_gcode_command("T0")
        elif extruder == "right":
            self.write_gcode_command("T1")

    def get_fan_speed(self, fan):
        return self.information['fan'][fan]['speed']

    @pyqtSlot(str, float)
    def set_fan_speed(self, fan, speed):
        """
        Gcode: M106 - Set print fan speed.
        """
        command = "M106"
        if 'left' in fan:
            command += " P0"
        elif 'right' in fan:
            command += " P1"
        elif 'exhaust' in fan:
            command += " P2"
        command += " S" + str(int(speed * 255))
        self.write_gcode_command(command)

    @pyqtSlot(result=float)
    def set_led_light(self):
        return self.information['led']['light']

    @pyqtSlot(float)
    def set_led_light(self, light):
        """
        Gcode: M355 - Set Case Light on/off and set brightness.
        """
        command = "M355"
        command += " S" + str(int(light * 255))
        self.write_gcode_command(command)

    @pyqtSlot(result=float)
    def get_position(self, axis: str):
        if axis in "XYZE":
            return self.information['motor']['position'][axis]

        return 0

    def connect_check(self):
        if self.is_connected():
            self.connect_check_timer.stop()
        else:
            self._sendCommand("G0\n")

    def connect_check_timeout(self):
        self.connect_check_timer.stop()
        if not self.is_connected():
            logging.warning(F"Printer connection failed.")
            self.serial_close()

    @pyqtSlot()
    def print_pause(self):
        if self._is_printing:
            logging.debug(F"Pause printing.")
            self._sendCommand('M76')
            self._sendCommand('G91')
            self._sendCommand('G1 Z10')
            self._sendCommand('G90')
            self._is_paused = True
            self.printing_information = {
                "speed": 0.0,
                "motor": {"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0},
                "temperature": {"left": 0, "right": 0, "bed": 0, "chamber": 0},
                "fan": {"left": 0.0, "right": 0.0, "chamber": 0.0}
            }

    @pyqtSlot()
    def print_resume(self):
        if self._is_printing:
            logging.debug(F"Resume printing.")
            self._sendCommand('G91')
            self._sendCommand('G1 Z-10')
            self._sendCommand('G90')
            self._sendCommand('M75')
            self._is_paused = False
            self._sendNextGcodeLine()

    @pyqtSlot()
    def print_stop(self):
        logging.debug(F"Stop printing.")
        self._gcode_position = 0
        self._gcode.clear()
        self._is_printing = False
        self._is_paused = False
        while not self._command_queue.empty():
            self._command_queue.get()

        self._sendCommand('M108\nM140 S0\nM141 S0\nM104 T0 S0\nM104 T1 S0\nM107 P0\nM107 P1\nG28XY\nM400\nM77\nM84')
        self.updatePrinterStatus.emit(1)

    @pyqtSlot(str)
    def print_start(self, path):
        logging.debug(F"Start print {path}.")
        # file = QFile()
        self.print_file = path
        if 'file:' in path:
            if platform.system().lower() == 'windows':
                path = path[8:]
            elif platform.system().lower() == 'linux':
                path = path[7:]
        # file.setFileName(path)
        # if not file.open(QIODevice.ReadOnly | QIODevice.Text):
        #     logging.warning(F"Print file open failed.")
        #     return
        # self._gcode.clear()
        # self._gcode.extend(str(file.readAll(), encoding='utf-8').split("\n"))
        with open(path, 'rt') as f:
            self._gcode.clear()
            self._gcode.extend(f.read().split("\n"))
            f.close()

        # Reset line number. If this is not done, first line is sometimes ignored
        self._gcode.insert(0, "M110")
        self._gcode_position = 0

        if self.get_extruder() == 'right':
            self._sendCommand('M84\nG28\nT0\nG0 Y319 F6600')
        self._sendCommand('M75')

        for i in range(0, 4):  # Push first 4 entries before accepting other inputs
            self._sendNextGcodeLine()

        self.printing_information['path'] = path

        self.updatePrinterStatus.emit(2)
        self._is_paused = False
        self._is_printing = True

        # file.close()
        # del file

    @pyqtSlot()
    def print_again(self):
        if self.print_file:
            logging.debug(F"Print again.")
            self.print_start(self.print_file)

    @pyqtSlot()
    def printer_reboot(self):
        logging.debug(F"Reboot printer.")
        self._sendCommand(b'D0\n')  # Reboot
        self.serial_close()

    @pyqtSlot(result=bool)
    def is_printing(self):
        return self._is_printing

    @pyqtSlot(result=bool)
    def is_paused(self):
        return self._is_printing and self._is_paused

    @pyqtSlot(result=bool)
    def printer_all_homed(self):
        return self.information['home']['X'] and self.information['home']['Y'] and self.information['home']['Z']

    @pyqtSlot(result=float)
    def print_progress(self):
        try:
            progress = self._gcode_position / len(self._gcode)
            return round(progress, 2)
        except ZeroDivisionError:
            logging.error("Error: no gcode data !")
            return 0

    @pyqtSlot(result=bool)
    def get_level_state(self):
        return self.leveling_working

    @pyqtSlot(bool)
    def set_level_state(self, state=0):
        self.leveling_working = state
        if self.leveling_working:
            self.information['bedMesh'] = []

    @pyqtSlot(result=int)
    def get_filament_state(self):
        return self.filament_working

    @pyqtSlot(int)
    def set_filament_state(self, state=0):
        self.filament_working = state

    @pyqtSlot(str, result=str)
    def get_ip_addr(self, name="lo"):
        if name in netifaces.interfaces():
            return netifaces.ifaddresses(name).get(netifaces.AF_INET)[0]['addr']

    @pyqtSlot(result=str)
    def version(self):
        return self._version

    @pyqtSlot()
    def onTimerTriggered(self):
        if not self.is_connected() and not self.is_connecting():
            self.connect_serial()

    def set_dial_indicator_value(self, obj, value):
        self.dial_indicator[obj] = float(value)

    def save_right_offset(self, axis: str, offset: float):
        self.write_gcode_command(f"M218 T1 {axis}{offset}\nM500\nM218")

    def save_dial_indicator_value(self):
        offset = self.information['probe']['offset']['right']['Z'] + self.dial_indicator['left'] - self.dial_indicator[
            'right']
        self.save_right_offset('Z', offset)

    @pyqtSlot()
    def print_verify(self):
        logging.debug(F"Start print verify.")
        path = "resource/gcode/print_verify.gcode"
        with open(path, 'rt') as f:
            self._gcode.clear()
            self._gcode.extend(f.read().split("\n"))
            f.close()

        # Reset line number. If this is not done, first line is sometimes ignored
        self._gcode.insert(0, "M110")
        self._gcode_position = 0
        # Push first 4 entries before accepting other inputs
        for i in range(0, 4):
            self._sendNextGcodeLine()

        self._is_print_verify = True

    @pyqtSlot()
    def is_print_verify(self):
        return self._is_print_verify
