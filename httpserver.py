import json
import socket
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from settings import *


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def get_json_string(path):
        try:
            with open(path, 'r') as json_file:
                return json_file.read()
        except Exception as e:
            return '{"exception": "%s"}' % e

    def return_json(self):
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

try:
    import termios
    import tty
    def getch():

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
except:
        import msvcrt
        def getch():
            return msvcrt.getch().decode("utf-8")


def listen_keys():
    print(f'Press <{SEND_DATAGRAM_KEY}> to send UDP datagram to {CLIENT_ADDRESS}:{CLIENT_PORT}')
    print(f'Press <{STOP_KEYLISTENING_KEY}> to stop listen keyboard')
    button_delay = 0.2

    while True:
        char = getch()

        if (char == STOP_KEYLISTENING_KEY):
            print("Key listening was stopped.")
            print("Now you can press <Ctrl+c> to stop script.")
            exit(0)

        if (char == SEND_DATAGRAM_KEY):
            time.sleep(button_delay)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((CLIENT_ADDRESS, CLIENT_PORT))
            print("UPD socket was connected")
            sock.send(b'ok')
            print("UPD package was send")
            sock.close()
            print("UPD socket was disconnected")


if __name__ == '__main__':
    server_thread = threading.Thread(target=run)
    server_thread.start()
    print(f'Python server started on {SERVER_ADDRESS}:{SERVER_PORT}')
    keyboard_thread = threading.Thread(target=listen_keys)
    keyboard_thread.start()
