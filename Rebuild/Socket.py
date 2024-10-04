from flask import Flask
from flask_socketio import SocketIO, send, emit
import threading

class Socket(threading.Thread):
    app = None
    socketio = None
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()


    def callback(self):
        self.root.quit()
    

    def run(self):
        print('socket running')
        app = Flask(__name__)
        host = '0.0.0.0'
        port = '8080'
        debug = True
        socketio = SocketIO(app, cors_allowed_origins="*")
        socketio.run(app, host=host, port=port, debug=debug)