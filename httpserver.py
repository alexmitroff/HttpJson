import json
from http.server import *


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    JSON_DATA = {
            'students': [
                {
                    'id': 3,
                    'fullname': u'Имя Фамилия',
                    'rank': 'генерал вся руси',
                    'group': '7'
                },
                {
                    'id': 1,
                    'fullname': 'John Doe',
                    'rank': 'генерал',
                    'group': '7'
                },
            ],
            'groups': [
                {
                    'id': 7,
                    'name': 'Первая учебная'
                },
                {
                    'id': 8,
                    'name': 'Вторая полевая'
                },
            ]
        }

    def return_json(self):
        serialized_json = json.dumps(self.JSON_DATA)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(serialized_json.encode('utf-8'))

    def do_GET(self):
        self.return_json()

    def do_POST(self):
        self.return_json()


def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
