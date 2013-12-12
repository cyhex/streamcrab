__author__ = 'gx'

from flask import Flask, render_template, Response, request
from smm import config
from smm import models
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
import gevent
import logging
logger = logging.getLogger(__name__)


gevent.monkey.patch_all()

app = Flask(__name__, template_folder=config.server_templates, static_folder= config.server_static)
app.debug = config.server_debug

models.connect()

@app.route('/')
def index():
    return render_template('index.html')


class StreamNamespace(BaseNamespace):

    def fetch_stream(self):
        self.last_id = None
        while True:
            for c in models.ClassifiedStream.find_tokens(self.track_kw, self.last_id)[0:25]:
                self.emit('stream_update', c.to_dict())
                self.last_id = c.id

            gevent.sleep(0.1)

    def on_track(self, data):
        self.track_kw = data
        self.spawn(self.fetch_stream())


@app.route('/socket.io/<path:remaining>')
def stream(remaining):
    try:
        socketio_manage(request.environ, {'/stream': StreamNamespace}, request)
    except:
        logger.error("Exception while handling socketio connection", exc_info=True)

    return Response()