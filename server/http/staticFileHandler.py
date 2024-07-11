import os

import tornado

from server.http import RequestHandler


class StaticFileHandler(tornado.web.StaticFileHandler):
    async def delete(self, path):
        # Set up our path instance variables.
        self.path = self.parse_url_path(path)
        del path  # make sure we don't refer to path instead of self.path again
        absolute_path = self.get_absolute_path(self.root, self.path)
        self.absolute_path = self.validate_absolute_path(self.root, absolute_path)
        if self.absolute_path is None:
            return
        if os.path.isfile(self.absolute_path):
            os.remove(self.absolute_path)
        else:
            self.write_error(400, f"Invalid file path: {self.absolute_path}")
        res_info = {'result': {
            "action": "delete_file",
            "item": {
                "path": os.path.basename(self.absolute_path),
                "root": "gcodes",
                "size": 0,
                "modified": 0,
                "permissions": ""
            }
        }}
        self.write(res_info)

    def set_default_headers(self):
        # 设置Access Control Allow的域，*代表允许任何域
        self.set_header('Access-Control-Allow-Origin', '*')
        # 设置Access Control Allow的方法
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        # 设置Access Control Allow的Headers
        self.set_header('Access-Control-Allow-Headers', '*')

    def options(self, path):
        self.set_status(204)
        self.finish()
