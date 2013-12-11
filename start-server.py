from gevent import monkey
from socketio.server import SocketIOServer

from smm import config
from smm.server import app

monkey.patch_all()

SocketIOServer(('', 5000), app, resource="socket.io",
               transports=config.server_socketio_handlers,
               policy_server=False
).serve_forever()