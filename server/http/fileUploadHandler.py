import tornado.ioloop
import tornado.web

from server.http import RequestHandler


class FileUploadHandler(RequestHandler):
    def post(self):
        # 使用self.request.files来访问上传的文件
        root_path = self.get_body_argument("path", self.get_body_argument("root", "gcodes"))
        files = self.request.files['file']  # 'file'是表单中的input元素name属性值

        # for file in files:
        # 只上传了一个文件
        uploaded_file = files[0]
        file_name = f'{root_path}/{uploaded_file["filename"]}'
        data = uploaded_file['body']

        root, dir_path = self._convert_request_path(file_name)

        # 处理文件，例如保存到磁盘
        with open(dir_path, 'wb') as f:
            f.write(data)

        self.write_results(self._sched_changed_event("create_file", root, dir_path))
