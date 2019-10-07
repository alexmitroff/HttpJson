# Simple Python Http server and client for Delphi 7 tests

## Installation
Clone or download project
```bash
cd HttpJson
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Setup
Edit **settings.py**
```python
# Python server self address:
SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8000

# Send UDP datagram to:
CLIENT_ADDRESS = '192.168.0.2'
CLIENT_PORT = 6625

SEND_DATAGRAM_KEY = 'q'
STOP_KEYLISTENING_KEY = 'p'

JSON_FILE_PATH = './example.json'
```

## Run
```bash
cd HttpJson
source venv/bin/activate
python httpserver.py
```