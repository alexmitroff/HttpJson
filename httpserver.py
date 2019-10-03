import json
from http.server import *
from http.client import *
from urllib.parse import parse_qs
import socket
import threading
import sys, termios, tty, os, time


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
        serialized_json = json.dumps(self.JSON_DATA, ensure_ascii=False)
        print(serialized_json)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(serialized_json.encode('utf-8'))

    def do_GET(self):
        self.return_json()

    def do_POST(self):
        # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # if ctype == 'multipart/form-data':
        #     postvars = cgi.parse_multipart(self.rfile, pdict)
        #     print(postvars)
        #     self.send_response(200)

        length = self.headers['content-length']
        data = self.rfile.read(int(length)).decode('utf-8')
        fields = parse_qs(data)
        print(fields)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'starts': True}).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler):
    server_address = ('192.168.0.104', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def send_request():
    connection = HTTPConnection('https://192.168.1.1')
    connection.request("GET", '/')


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
            UDP_HOST = '192.168.0.102'
            UDP_PORT = 6625
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((UDP_HOST, UDP_PORT))
            print("UPD socket connected")
            sock.send(b'ok')
            print("UPD package was send")
            sock.close()
            print("UPD socket closed")


if __name__ == '__main__':
    # keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))
    serverthread = threading.Thread(target=run)
    serverthread.start()
    # run()
    keyboardthread = threading.Thread(target=listen_keys)
    keyboardthread.start()
