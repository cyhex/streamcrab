from numpy.distutils.command.config import config
from smm.models import SocketSession

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

app = Flask(__name__, template_folder=config.server_templates, static_folder=config.server_static)
app.debug = config.server_debug

models.connect()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def results():
    keyword = request.args.get('keyword', '')
    return render_template('results.html', keyword=keyword)


class StreamNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(StreamNamespace, self).__init__(*args, **kwargs)
        self.tokenizer = config.classifier_tokenizer
        self.logger = logging.getLogger(self.__class__.__name__)
        self.socket_session = None

    def can_connect(self):
        SocketSession.remove_expired()
        if models.SocketSession.objects(ip=self.environ.get('REMOTE_ADDR')).count() >= config.server_max_connection_per_ip:
            error_msg = 'You have reached the limit of %d open sockets per IP' % config.server_max_connection_per_ip
            self.emit('error', error_msg)
            self.logger.debug('Disconnected: %s', error_msg)
            return False

    def recv_connect(self):
        self.can_connect();
        self.logger.debug('Connect from %s', str(self.socket))
        self.socket_session = models.SocketSession()
        self.socket_session.ip = self.environ.get('REMOTE_ADDR')
        self.socket_session.save()


    def on_track(self, track):

        tokens = list(self.tokenizer.getSearchTokens(track))
        if not tokens:
            return True

        self.socket_session.keywords = list(self.tokenizer.getSearchTokens(track))
        self.socket_session.save()
        self.logger.debug('Track %s from %s', tokens, str(self.socket))

        def fetch_stream():
            self.last_id = None
            while True:
                for c in models.ClassifiedStream.find_tokens(self.socket_session.keywords, self.last_id):
                    self.emit('stream_update', c.to_dict())
                    self.last_id = c.id

                gevent.sleep(1)

        self.spawn(fetch_stream)

    def recv_disconnect(self):
        if self.socket_session:
            self.socket_session.delete()
        self.logger.debug('Disconnect from %s', str(self.socket))
        self.disconnect(silent=True)

    def on_ping(self):
        self.logger.debug('Ping from %s', str(self.socket))
        if self.socket_session:
            self.socket_session.ping()


@app.route('/socket.io/<path:remaining>')
def stream(remaining):
    try:
        socketio_manage(request.environ, {'/stream': StreamNamespace}, request)
    except:
        logger.error("Exception while handling socketio connection", exc_info=True)

    return Response()