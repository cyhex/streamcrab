from socketio.server import SocketIOServer
from gevent import monkey

from smm import config
from smm.server import app
import logging
logger = logging.getLogger('')

monkey.patch_all()

try:
    server = SocketIOServer((config.server_host, config.server_port), app, resource="socket.io",
                            transports=config.server_socketio_handlers, policy_server=False)
    logger.info('Serving at http://%s:%s' % (config.server_host, config.server_port))
    server.serve_forever()

except (KeyboardInterrupt, SystemExit):
    server.stop()