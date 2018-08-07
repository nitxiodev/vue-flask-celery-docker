from gevent.monkey import patch_all
patch_all()

from celery import Celery
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def createApp(config, socket_io=False):
    app = Flask(__name__)
    app.config.from_object(config)

    if socket_io:
        socketio.init_app(app, message_queue=app.config['SOCKETIO_BROKER_URL'])

    return app

# Config mode
DEPLOY_MODE = 'countdown_backend.src.server.config.ProductionConfig'
FLASK_SERVER_PORT = 8888
SOCKETIO_SERVER_PORT = 8000

# Main Flask app
app = createApp(DEPLOY_MODE)

# Configure celery
celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
