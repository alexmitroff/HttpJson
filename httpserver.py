import json
import socket
import sys
import termios
import threading
import time
import tty
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from .settings import SERVER_ADDRESS, SERVER_PORT, CLIENT_ADDRESS, CLIENT_PORT, JSON_FILE_PATH


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

    @staticmethod
    def get_json_string(path):
        try:
            with open(path, 'r') as json_file:
                return json_file.read()
        except Exception as e:
            return '{"exception": "%s"}' % e

    def return_json(self):
        # serialized_json = json.dumps(self.JSON_DATA, ensure_ascii=False)
        serialized_json = self.get_json_string(JSON_FILE_PATH)
        print(serialized_json)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(serialized_json.encode('utf-8'))

    def do_GET(self):
        self.return_json()

    def do_POST(self):
        length = self.headers['content-length']
        data = self.rfile.read(int(length)).decode('utf-8')
        fields = parse_qs(data)
        print(fields)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'starts': True}).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler):
    server_address = (SERVER_ADDRESS, SERVER_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def listen_keys():
    button_delay = 0.2

    while True:
        char = getch()

        if (char == "p"):
            print("Stop!")
            exit(0)

        if (char == "q"):
            time.sleep(button_delay)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((CLIENT_ADDRESS, CLIENT_PORT))
            print("UPD socket connected")
            sock.send(b'ok')
            print("UPD package was send")
            sock.close()
            print("UPD socket closed")


if __name__ == '__main__':
    # run()
    server_thread = threading.Thread(target=run)
    server_thread.start()
    keyboard_thread = threading.Thread(target=listen_keys)
    keyboard_thread.start()
