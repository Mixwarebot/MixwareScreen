import json
import os
import shutil
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import tornado

from qtCore import is_release

StrOrPath = Union[str, Path]
VALID_GCODE_EXTS = ['.gcodes', '.g', '.gco', '.ufp', '.nc']


class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(404)


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self, path: str):
        self.file_paths: Dict[str, str] = {}
        if not is_release:
            dp: str = "E:/RODEO/Firmware/KD7/mixwareScreen/resource"
        else:
            moonraker_data_path = os.getenv("MOONRAKER_DATA_PATH")
            dp: str = moonraker_data_path or "~/printer_data"

        self.data_path = Path(dp).expanduser().resolve()
        self.gcodes_path = self.data_path.joinpath(path)
        self.file_paths[path] = str(self.gcodes_path)

    def _convert_request_path(self, request_path: str) -> Tuple[str, str]:
        # Parse the root, relative path, and disk path from a remote request
        separator = '/' if is_release else '\\'
        parts = os.path.normpath(request_path).strip(separator).split(separator, 1)
        if not parts:
            raise tornado.web.HTTPError(400, reason=f"Invalid path: {request_path}")
        root = parts[0]
        if root not in self.file_paths:
            raise tornado.web.HTTPError(400, reason=f"Invalid root path ({root})")
        root_path = dest_path = self.file_paths[root]
        if len(parts) > 1:
            dest_path = os.path.abspath(os.path.join(dest_path, parts[1]))
            if not dest_path.startswith(root_path):
                raise tornado.web.HTTPError(400, reason=
                f"Invalid path request, '{request_path}'' is outside "
                f"root '{root}'")
        return root, dest_path

    def _list_directory(self,
                        path: str,
                        root: str,
                        is_extended: bool = False
                        ) -> Dict[str, Any]:
        if not os.path.isdir(path):
            raise tornado.web.HTTPError(400, reason=f"Directory does not exist ({path})")
        # self.check_reserved_path(path, False)
        flist: Dict[str, Any] = {'dirs': [], 'files': []}
        for fname in os.listdir(path):
            full_path = os.path.join(path, fname)
            if not os.path.exists(full_path):
                continue
            path_info = self.get_path_info(full_path, root)
            if os.path.isdir(full_path):
                path_info['dirname'] = fname
                flist['dirs'].append(path_info)
            elif os.path.isfile(full_path):
                path_info['filename'] = fname
                # Check to see if a filelist update is necessary
                # ext = os.path.splitext(fname)[-1].lower()
                # if (
                #         root == "gcodes" and
                #         ext in VALID_GCODE_EXTS and
                #         is_extended
                # ):
                #     rel_path = self.get_relative_path(root, full_path)
                #     metadata: Dict[str, Any] = self.gcode_metadata.get(
                #         rel_path, {})
                #     path_info.update(metadata)
                flist['files'].append(path_info)
        usage = shutil.disk_usage(path)
        flist['disk_usage'] = usage._asdict()
        flist['root_info'] = {
            'name': root,
            'permissions': "rw"  # if root in self.full_access_roots else "r"
        }
        return flist

    def get_path_info(
            self, path: StrOrPath, root: str, raise_error: bool = True
    ) -> Dict[str, Any]:
        if isinstance(path, str):
            path = Path(path)
        real_path = path.resolve()
        try:
            fstat = path.stat()
        except Exception:
            if raise_error:
                raise
            return {"modified": 0, "size": 0, "permissions": ""}
        if ".git" in real_path.parts:
            permissions = ""
        else:
            permissions = "rw"
            # if (
            #         root not in self.full_access_roots or
            #         (path.is_symlink() and path.is_file())
            # ):
            #     permissions = "r"
            # for name, (res_path, can_read) in self.reserved_paths.items():
            #     if (res_path == real_path or res_path in real_path.parents):
            #         if not can_read:
            #             permissions = ""
            #             break
            #         permissions = "r"
        return {
            'modified': fstat.st_mtime,
            'size': fstat.st_size,
            'permissions': permissions
        }

    def get_relative_path(self, root: str, full_path: str) -> str:
        root_dir = self.file_paths.get(root, None)
        if root_dir is None or not full_path.startswith(root_dir):
            return ""
        return os.path.relpath(full_path, start=root_dir)

    def _sched_changed_event(
            self,
            action: str,
            root: str,
            full_path: str,
            source_root: Optional[str] = None,
            source_path: Optional[str] = None,
            immediate: bool = False
    ) -> Dict[str, Any]:
        rel_path = self.get_relative_path(root, full_path)
        path_info = self.get_path_info(full_path, root, raise_error=False)
        path_info.update({"path": rel_path, "root": root})
        notify_info: Dict[str, Any] = {
            "action": action,
            "item": path_info
        }
        # if source_path is not None and source_root is not None:
        #     src_rel_path = self.get_relative_path(source_root, source_path)
        #     notify_info['source_item'] = {'path': src_rel_path, 'root': source_root}
        # immediate |= not self.fs_observer.has_fast_observe
        # delay = .005 if immediate else 1.
        # key = f"{action}-{root}-{rel_path}"
        # handle = self.event_loop.delay_callback(
        #     delay, self._do_notify, key, notify_info
        # )
        # if not immediate:
        #     self.scheduled_notifications[key] = handle
        return notify_info

    def write_results(self, info: Dict[str, Any]):
        res_info = {'result': info}
        self.write(res_info)

    def write_error(self, status_code: int, **kwargs) -> None:
        err = {'code': status_code, 'message': self._reason}
        if 'exc_info' in kwargs:
            err['traceback'] = "\n".join(
                traceback.format_exception(*kwargs['exc_info']))
        self.finish(json.dumps({'error': err}))

    def set_default_headers(self):
        # 设置Access Control Allow的域，*代表允许任何域
        self.set_header('Access-Control-Allow-Origin', '*')
        # 设置Access Control Allow的方法
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        # 设置Access Control Allow的Headers
        self.set_header('Access-Control-Allow-Headers', '*')
        # 设置Access Content Type
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def options(self):
        self.set_status(204)
        self.finish()
