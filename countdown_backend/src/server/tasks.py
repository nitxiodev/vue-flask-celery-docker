import celery
from celery.exceptions import Reject
from flask_socketio import SocketIO

from countdown_backend.src.server import ServiceException
from countdown_backend.src.server.NumbersService import NumberService
from countdown_backend.src.server.flask_inits import app


class CeleryTask(celery.Task):
    name = __name__
    serializer = 'json'
    ignore_result = False

    def __init__(self):
        self._numbers_service = NumberService()
        super(CeleryTask, self).__init__()

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(CeleryTask, self).__call__(*args, **kwargs)#self.run(*args, **kwargs)

    def run(self, numbers, target, client_id, message_queue, *args, **kwargs):
        self.update_state(state='PROGRESS', meta={})
        try:
            solution, recursions, exec_time = self._numbers_service.solve(target, numbers)
            msg = {
                'solution': solution,
                'recursions': recursions,
                'exec_time': exec_time
            }

            # Websockets support
            local_socketio = SocketIO(message_queue=message_queue)
            local_socketio.emit('solution', msg, room=client_id)
            return msg
        except ServiceException as f:
            self.update_state(state='FAILURE', meta={'exc_type': '', 'exc_message': (f.errorcode.value, f.message)})
            raise Reject()
