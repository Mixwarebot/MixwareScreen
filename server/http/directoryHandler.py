import json
import os
import platform
import shutil
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import tornado

from qtCore import is_release
from server.http import RequestHandler


class DirectoryHandler(RequestHandler):
    async def get(self):
        directory = self.get_query_argument('path', "gcodes")
        root, dir_path = self._convert_request_path(directory)
        is_extended = bool(self.get_query_argument('extended', False))
        self.write_results(self._list_directory(dir_path, root, is_extended))

    async def post(self):
        # Create a new directory
        directory = self.get_query_argument('path', "gcodes")
        root, dir_path = self._convert_request_path(directory)
        print('Create a new directory', root, dir_path, directory)
        try:
            os.mkdir(dir_path)
        except Exception as e:
            raise tornado.web.HTTPError(400, reason=str(e))
        self.write_results(self._sched_changed_event("create_dir", root, dir_path))

    async def delete(self):
        directory = self.get_query_argument('path', "gcodes")
        root, dir_path = self._convert_request_path(directory)
        if directory.strip("/") == root:
            raise tornado.web.HTTPError(400, reason=
            "Cannot delete root directory")
        if not os.path.isdir(dir_path):
            raise tornado.web.HTTPError(400, reason=
            f"Directory does not exist ({directory})")
        force = self.get_query_argument('force', 'false')
        if force == 'true':
            # Make sure that the directory does not contain a file
            # loaded by the virtual_sdcard
            # self._handle_operation_check(dir_path)
            try:
                shutil.rmtree(dir_path)
            except Exception:
                raise
        else:
            try:
                os.rmdir(dir_path)
            except Exception as e:
                raise tornado.web.HTTPError(400, reason=str(e))

        self.write_results(self._sched_changed_event("delete_dir", root, dir_path))
