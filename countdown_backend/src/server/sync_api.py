from flask import Blueprint, jsonify
from flask import request

from countdown_backend.src.server import ServiceException, ServiceCodes
from countdown_backend.src.server.NumbersService import NumberService


class CountdownSyncAPI(Blueprint):
    def __init__(self, *args):
        self._numbers_service = NumberService()
        self._config = None
        super(CountdownSyncAPI, self).__init__(*args)

        @self.route('/numbers_sync', methods=['POST'])
        def solver():
            data = request.get_json(silent=True)

            if data is None:
                ret = {
                    'msg': 'Data must be encoded in a JSON object!',
                    'code': 422
                }
            else:
                numbers = data.get('numbers')
                target = data.get('target')

                try:
                    solution, recursions, exec_time = self._numbers_service.solve(target, numbers)
                    ret = {
                        'msg': {
                            'solution': solution,
                            'recursions': recursions,
                            'exec_time(s)': exec_time
                        },
                        'code': 200
                    }
                except ServiceException as f:
                    if f.errorcode == ServiceCodes.EMPTY_PARAMS:
                        ret = {
                            'msg': 'Some or every parameters are empty!',
                            'code': 422
                        }
                    else:
                        ret = {
                            'msg': f.message,
                            'code': 409
                        }
            code = ret.pop('code')
            return jsonify(ret['msg']), code

    def register(self, app, options, first_registration=False):
        super(CountdownSyncAPI, self).register(app, options, first_registration)
        self._config = app.config
