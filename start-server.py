from socketio.server import SocketIOServer
import gevent
from gevent import monkey

from smm import config
from smm.server import app

monkey.patch_all()

try:
    server = SocketIOServer(('', 5000), app, namespace="socket.io",
                            transports=config.server_socketio_handlers, policy_server=False)
    server.serve_forever()

except (KeyboardInterrupt, SystemExit):
    server.stop()