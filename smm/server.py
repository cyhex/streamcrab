__author__ = 'gx'

from flask import Flask, render_template, Response, request
from smm import config
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
import gevent
import logging
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=config.server_templates, static_folder= config.server_static)
app.debug = config.server_debug

@app.route('/')
def index():
    return render_template('index.html')


class StreamNamespace(BaseNamespace):

    def sendcpu(self):
        prev = None
        while True:
            self.emit('cpu_data', self.data)
            gevent.sleep(1)

    def on_track(self, data):
        self.data = data
        self.spawn(self.sendcpu())


@app.route('/socket.io/<path:remaining>')
def stream(remaining):
    try:
        socketio_manage(request.environ, {'/stream': StreamNamespace}, request)
    except:
        logger.error("Exception while handling socketio connection", exc_info=True)

    return Response()