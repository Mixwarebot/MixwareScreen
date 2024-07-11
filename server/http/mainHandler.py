import tornado

from server.http import RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        # print(self.request.host)
        # print(self.request.method)
        # print(self.request.uri)
        # print(self.request.version)
        # print(self.request.remote_ip)
        # print(self.get_query_argument('path', 'null'))
        # print(self.get_query_argument('extended', 'null'))
        # print(self.get_body_argument('extended', 'false'))
        self.write("Hello, world")
