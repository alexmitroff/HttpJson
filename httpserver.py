import json
from http.server import *


class CustomHTTPRequstHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        data = {
            'students': [
                {
                    'id': 1,
                    'fullname': 'Имя Фамилия',
                    'rank': 'генерал вся руси',
                    'role': 'teacher',
                    'group': '7'
                },
                {
                    'id': 1,
                    'fullname': 'John Doe',
                    'rank': 'генерал',
                    'role': 'student',
                    'group': '7'
                },
            ],
            'groups': [
                {
                    'id': 7,
                    'fullname': 'Первая учебная'
                },
                {
                    'id': 8,
                    'fullname': 'Вторая полевая'
                },
            ]
        }

        serialized_json = json.dumps(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(serialized_json.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=CustomHTTPRequstHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
