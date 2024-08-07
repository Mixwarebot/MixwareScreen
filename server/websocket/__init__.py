import json
import logging
from typing import Any, Dict, List, Union

import tornado
from PyQt5.QtCore import QObject, pyqtSlot
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

websocket_clients = set()


class WebSocket(WebSocketHandler):
    printer = None
    subscribe = {}

    def initialize(self, printer):
        self.printer = printer

    def open(self):
        self.set_nodelay(True)
        websocket_clients.add(self)
        print(F'WebSocket {self.request.host_name} connect')

    def on_message(self, message):
        IOLoop.current().add_callback(self._process_message, message)
        try:
            data: Union[Dict[str, Any], List[dict]] = json.loads(message)
        except Exception:
            # if isinstance(message, bytes):
            # data = message.decode()
            logging.exception(f"data not valid json: {message}")
            err = self.build_error(-32700, "Parse error")
            return json.dumps(err).encode("utf-8")

    def on_close(self):
        print(F'WebSocket {self.request.host_name} disconnect')
        websocket_clients.remove(self)

    def check_origin(self, origin):
        return True

    def _process_message(self, message):
        data: Union[Dict[str, Any], List[dict]] = json.loads(message)
        if 'method' in data:
            if data['method'] == 'printer.gcode.script':
                try:
                    self.printer.write_gcode_command(data['params']['script'])
                    self.notify_gcode_response(data['id'] if 'id' in data else -1)
                except:
                    print('No params')
            elif data['method'] == 'printer.objects.subscribe':
                try:
                    for obj in data['params']['objects']:
                        if type(data['params']['objects'][obj]) == list:
                            self.subscribe[obj] = {}
                            for subObj in data['params']['objects'][obj]:
                                self.subscribe[obj][subObj] = None
                        elif type(data['params']['objects'][obj]) == str:
                            self.subscribe[obj] = {}
                            self.subscribe[obj][data['params']['objects'][obj]] = None
                        else:
                            self.subscribe[obj] = None
                    self.notify_status_update()
                except:
                    print('objects null')
            elif data['method'] == 'printer.print.start':
                try:
                    self.printer.print_start(data['params']['filename'])
                except:
                    print('Failed to start printing, file does not exist.')
            elif data['method'] == 'printer.print.pause':
                self.printer.print_pause()
            elif data['method'] == 'printer.print.resume':
                self.printer.print_resume()
            elif data['method'] == 'printer.print.cancel':
                self.printer.print_stop()
        else:
            print('No method')

    def write_jsonrpc(self, method, params=None, id=-1):
        message = {
            'jsonrpc': '2.0',
            'method': method,
        }
        if params:
            message['params'] = params
        if id != -1:
            message['id'] = id
        self.write_message(message)

    def notify_status_update(self):
        self.subscribe_update()
        packet = {
            'jsonrpc': '2.0',
            'method': 'notify_status_update',
            'params': {
                'status': self.subscribe,
                'eventtime': tornado.ioloop.IOLoop.current().time(),
            }
        }
        self.write_message(packet)

    def notify_gcode_response(self, id=-1):
        self.write_jsonrpc('notify_gcode_response', 'ok', id)

    def subscribe_update(self):
        # if 'bed_mesh' in self.subscribe:
        #     if 'profiles' in self.subscribe['bed_mesh']:
        #         self.subscribe['bed_mesh']['profiles'] = self.printer.printing_information['bedMesh']

        if 'toolhead' in self.subscribe:
            if 'homed_axes' in self.subscribe['toolhead']:
                self.subscribe['toolhead']['homed_axes'] = ""
                for axis in ['X', 'Y', 'Z']:
                    if self.printer.get_homed_axes(axis):
                        self.subscribe['toolhead']['homed_axes'] += axis
            if 'extruder' in self.subscribe['toolhead']:
                self.subscribe['toolhead'][
                    'extruder'] = self.printer.get_extruder()
            if 'position' in self.subscribe['toolhead']:
                self.subscribe['toolhead']['position'] = [
                    self.printer.get_position('X'),
                    self.printer.get_position('Y'),
                    self.printer.get_position('Z'),
                    self.printer.get_position('E'),
                ]

        if 'led' in self.subscribe:
            if 'light' in self.subscribe['led']:
                self.subscribe['led']['light'] = self.printer.get_led_light()

        if 'print_stats' in self.subscribe:
            if 'state' in self.subscribe['print_stats']:
                self.subscribe['print_stats']['state'] = self.printer.get_print_state()
            if 'filename' in self.subscribe['print_stats']:
                self.subscribe['print_stats']['filename'] = ""
            if 'total_duration' in self.subscribe['print_stats']:
                self.subscribe['print_stats']['total_duration'] = ""

        if 'virtual_sdcard' in self.subscribe:
            if 'progress' in self.subscribe['virtual_sdcard']:
                self.subscribe['virtual_sdcard']['progress'] = ""
            if 'file_position' in self.subscribe['virtual_sdcard']:
                self.subscribe['virtual_sdcard']['file_position'] = ""
            if 'is_active' in self.subscribe['virtual_sdcard']:
                self.subscribe['virtual_sdcard']['is_active'] = ""

        for extruder in ['left', 'right', 'bed', 'chamber']:
            if 'extruder_' + extruder in self.subscribe:
                if 'target' in self.subscribe['extruder_' + extruder]:
                    self.subscribe['extruder_' + extruder]['target'] = self.printer.get_target(extruder)
                if 'temperature' in self.subscribe['extruder_' + extruder]:
                    self.subscribe['extruder_' + extruder]['temperature'] = self.printer.get_temperature(extruder)

        for fan in ['left', 'right', 'chamber', 'leftCool', 'rightCool', 'exhaust']:
            if 'fan_' + fan in self.subscribe:
                if 'speed' in self.subscribe['fan_' + fan]:
                    self.subscribe['fan_' + fan]['speed'] = self.printer.get_fan_speed(fan)
