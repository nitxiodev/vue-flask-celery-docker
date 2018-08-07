from gevent.monkey import patch_all
patch_all()

from countdown_backend.src.server.tasks import CeleryTask
from gevent.pywsgi import WSGIServer
from countdown_backend.src.server.flask_inits import app, celery, FLASK_SERVER_PORT

from countdown_backend.src.server.async_api import CountdownAsyncAPI
from countdown_backend.src.server.sync_api import CountdownSyncAPI

from flask import jsonify
from flask_cors import CORS

# Instance and register celery task
celery_tasks = CeleryTask()
celery.register_task(celery_tasks)

# Import blueprints
sync_api = CountdownSyncAPI('sync_api', __name__)
async_api = CountdownAsyncAPI('async_api', __name__, celery=celery_tasks)

# Apply CORS on every blueprint
CORS(sync_api)
CORS(async_api)

# Register blueprints
app.register_blueprint(sync_api)
app.register_blueprint(async_api)


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({'msg': 'This resource does not exist'}), 404

if __name__ == '__main__':
    w = WSGIServer(('0.0.0.0', FLASK_SERVER_PORT), app)
    try:
        w.serve_forever()
    except KeyboardInterrupt:
        w.stop(timeout=10)
