from flask import Flask
from flask_socketio import SocketIO, send, emit

class Socket:
    app = None
    socketio = None
    def __init__(self, host, port, debug):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.socketio.run(self.app, host=host, port=port, debug=debug)
