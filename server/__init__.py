import os
import platform

import tornado
from qtCore import *
from server.http import PageNotFoundHandler
from server.http.directoryHandler import DirectoryHandler
from server.http.fileUploadHandler import FileUploadHandler
from server.http.mainHandler import MainHandler
from server.http.staticFileHandler import StaticFileHandler
from server.websocket import WebSocket, websocket_clients


class Server(QObject):
    def __init__(self, printer: QObject):
        super(Server, self).__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.notify_status_update)
        self.application = tornado.web.Application()
        self.gcode_path: str = 'gcodes'
        self.static_gcodes_path: str = "/home/hyper-x/printer_data" if is_release else "E:/RODEO/Firmware/KD7/mixwareScreen/resource"

    def start_server(self):
        # 创建Tornado应用
        self.application = tornado.web.Application([
            # http
            (r"/api", MainHandler),
            (r"/server/files/directory", DirectoryHandler, dict(path=self.gcode_path)),  # 文件管理
            (r"/server/files/upload", FileUploadHandler, dict(path=self.gcode_path)),
            (r"/server/files/(.*)", StaticFileHandler,  # 文件下载 os.path.join(os.path.dirname(__file__))
             {"path": self.static_gcodes_path}),
            # websocket
            (r'/websocket', WebSocket, dict(printer=self._printer)),
            # other
            ('.*', PageNotFoundHandler)
        ])

        self.application.listen(6688)
        tornado.ioloop.IOLoop.current().start()

    def notify_status_update(self):
        for client in websocket_clients:
            client.notify_status_update()
