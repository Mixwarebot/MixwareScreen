import logging
import platform
import re
import time
import traceback
from threading import Thread

from nmcli import device

from qtCore import *
from pywifi import const, PyWiFi, Profile


class DeviceWifi:
    def __init__(self):
        self.in_use = False
        self.ssid = ''
        self.bssid = ''
        self.mode = ''
        self.chan = 0
        self.freq = 0
        self.rate = 0
        self.signal = 0
        self.security = ''


class WlanConnectQThread(QThread):
    def __init__(self):
        super(WlanConnectQThread, self).__init__()
        self._passwd = ""
        self._ssid = ""

    # def __del__(self):
    #     self.wait()

    def set_connect_wifi(self, ssid, passwd):
        self._ssid = ssid
        self._passwd = passwd

    def _connect_wifi(self):
        try:
            device.wifi_connect(self._ssid, self._passwd)
        except Exception as e:
            logging.debug("wifi connect failed.", e)

    def run(self) -> None:
        self._connect_wifi()


class WlanListQThread(QThread):
    newWlanList = pyqtSignal(QVariant)

    def __init__(self):
        super(WlanListQThread, self).__init__()
        self.working = True
        self.deviceWifi = []

    # def __del__(self):
    #     self.working = False
    #     self.wait()

    def _get_wifi_list(self):
        try:
            if platform.system().lower() == 'linux':
                device.wifi_rescan()
                lists = device.wifi()
                if lists:
                    self.deviceWifi.clear()
                    for info in lists:
                        dat = re.findall("in_use=(.*), ssid='(.*)', bssid='(.*)', mode='(.*)', chan=(\\d*), freq=(\\d*), "
                                         "rate=(\\d*), signal=(\\d*), security='(.*)'", str(info))
                        if dat:
                            dev = {'in_use': True if "True" in dat[0][0] else False, 'ssid': dat[0][1], 'bssid': dat[0][2], 'mode': dat[0][3],
                                   'chan': int(dat[0][4]), 'freq': int(dat[0][5]), 'rate': int(dat[0][6]),
                                   'signal': int(dat[0][7]), 'security': dat[0][8]}
                            self.deviceWifi.append(dev)
                    self.newWlanList.emit(self.deviceWifi)
            if platform.system().lower() == 'windows': #test
                self.deviceWifi.clear()
                for i in range(10):
                    dev = {'in_use': False, 'ssid': 'test' + str(i), 'bssid': '0', 'mode': '1',
                           'chan': 20, 'freq': 2000, 'rate': 2000, 'signal': 100,
                           'security': 'WPA2'}
                    self.deviceWifi.append(dev)
                self.newWlanList.emit(self.deviceWifi)
        except Exception as e:
            logging.debug("not find wifi.", e)

    def is_working(self):
        return self.working

    def run(self) -> None:
        self._get_wifi_list()


class MixwareScreenWLAN(QObject):
    newWlanList = pyqtSignal(QVariant)

    def __init__(self):
        super(MixwareScreenWLAN, self).__init__()
        self._list_thread = WlanListQThread()
        self._list_thread.newWlanList.connect(self._newWlanList)
        self._connect_thread = WlanConnectQThread()

    @pyqtSlot()
    def update(self):
        self._list_thread.start()

    @pyqtSlot(str, str)
    def connect(self, ssid, passwd):
        self._connect_thread._ssid = ssid
        self._connect_thread._passwd = passwd
        self._connect_thread.start()

    @pyqtSlot(QVariant)
    def _newWlanList(self, _list=QVariant):
        self.newWlanList.emit(_list)
