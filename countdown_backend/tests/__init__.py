## Run with[.../numbers_solver/tests/$]: nosetests --with-coverage --cover-package=.. __init__.py
import json
import unittest

from celery.exceptions import Reject
from hamcrest import assert_that, equal_to, greater_than, instance_of, calling, raises, empty
from kombu.exceptions import OperationalError
from mock import mock

from countdown_backend.src.numbers_solver.numbers_backtracking import NumbersSolver
from countdown_backend.src.server import ServiceException, ServiceCodes
from countdown_backend.src.server.NumbersService import NumberService
from countdown_backend.src.server.flask_inits import createApp, celery
from countdown_backend.src.server.flask_server import app
from countdown_backend.src.server.flask_socketio_server import socketio
from countdown_backend.src.server.tasks import CeleryTask


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class testCeleryTask(unittest.TestCase):
    def setUp(self):
        celery.config_from_object('countdown_backend.src.server.config.TestConfig')
        self._celery_task = CeleryTask()

    @mock.patch('countdown_backend.src.server.tasks.NumberService.solve', autospec=True)
    def testRun(self, mock_class):
        with mock.patch('countdown_backend.src.server.tasks.CeleryTask.update_state'):
            mock_class.return_value = ([], 100, 0.3)
            recv = self._celery_task.run(1, 1, 1, None)

            assert_that(recv, equal_to({'exec_time': 0.3, 'recursions': 100, 'solution': []}))

    @mock.patch('countdown_backend.src.server.tasks.NumberService.solve', autospec=True)
    def testRunException(self, mock_class):
        with mock.patch('countdown_backend.src.server.tasks.CeleryTask.update_state'):
            mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
            assert_that(calling(self._celery_task.run).with_args(1, 1, 1, None), raises(Reject))


class testFlaskServer(unittest.TestCase):
    def setUp(self):
        app.config.from_object('countdown_backend.src.server.config.TestConfig')
        celery.config_from_object('countdown_backend.src.server.config.TestConfig')
        self._return_task = AttrDict()
        self._flask_app = app.test_client()

    def testApiNotFound(self):
        recv = self._flask_app.post('/not_found')
        assert_that(recv.status_code, equal_to(404))

    def testSyncApiNoData(self):
        recv = self._flask_app.post('/numbers_sync')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    @mock.patch('countdown_backend.src.server.sync_api.NumberService.solve', autospec=True)
    def testSyncDatawithEmptyParams(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.EMPTY_PARAMS, msg='')
        recv = self._flask_app.post('/numbers_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(422))

    @mock.patch('countdown_backend.src.server.sync_api.NumberService.solve', autospec=True)
    def testSyncDataFail(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
        recv = self._flask_app.post('/numbers_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(409))

    @mock.patch('countdown_backend.src.server.sync_api.NumberService.solve', autospec=True)
    def testSyncDataOk(self, mock_class):
        mock_class.return_value = ([], 100, 0.3)
        recv = self._flask_app.post('/numbers_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(200))
        assert_that(eval(recv.data), equal_to({'exec_time(s)': 0.3, 'recursions': 100, 'solution': []}))

    def testAsyncApiNoData(self):
        recv = self._flask_app.post('/numbers_async')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    @mock.patch('countdown_backend.src.server.flask_server.CeleryTask.delay', autospec=True)
    def testAsyncDatawithEmptyParams(self, mock_class):
        mock_class.side_effect = OperationalError
        recv = self._flask_app.post('/numbers_async', data=json.dumps(dict(numbers='1', target=1, id='1')),
                                    content_type='application/json')
        assert_that(recv.status_code, equal_to(503))

    @mock.patch('countdown_backend.src.server.flask_server.CeleryTask.delay', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['id'] = 444
        mock_class.return_value = self._return_task
        recv = self._flask_app.post('/numbers_async', data=json.dumps(dict(numbers='1', target=1, id='1')),
                                    content_type='application/json')
        assert_that(recv.status_code, equal_to(201))
        assert_that(eval(recv.data), equal_to(str(444)))

        del self._return_task['id']

    @mock.patch('countdown_backend.src.server.flask_server.CeleryTask.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = 444
        self._return_task['state'] = 'PENDING'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(404))
        assert_that(eval(recv.data)['status'], equal_to('PENDING'))

        del self._return_task['result']
        del self._return_task['state']

    @mock.patch('countdown_backend.src.server.flask_server.CeleryTask.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = [0, 1]
        self._return_task['state'] = 'FAILURE'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(400))
        assert_that(eval(recv.data)['status'], equal_to('FAILURE'))

        del self._return_task['result']
        del self._return_task['state']

    @mock.patch('countdown_backend.src.server.flask_server.CeleryTask.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = {'exec_time': 0.3, 'recursions': 100, 'solution': []}
        self._return_task['state'] = 'SUCCESS'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(200))
        assert_that(eval(recv.data)['status'], equal_to('SUCCESS'))

        del self._return_task['result']
        del self._return_task['state']


class testSocketIOServer(unittest.TestCase):
    def setUp(self):
        self._flask_app = createApp('countdown_backend.src.server.config.TestConfig', socket_io=True)
        self.app = socketio.test_client(self._flask_app)

    def testMyId(self):
        self.app.emit('my_id')
        recv = self.app.get_received()

        assert_that(recv[0]['args'][0], instance_of(str))
        assert_that(recv[0]['name'], equal_to('connected'))

    def testConnect(self):
        self.app.connect()
        recv = self.app.get_received()
        assert_that(recv, empty())

    def testDisconnect(self):
        self.app.disconnect()
        recv = self.app.get_received()
        assert_that(recv, empty())


class testNumbers(unittest.TestCase):
    def setUp(self):
        self._numbers = NumbersSolver()

    def tearDown(self):
        del self._numbers

    def testTargetSolution(self):
        solution, _, _ = self._numbers.lookup(844, [100, 75, 50, 25, 10, 8])
        assert_that(solution[-1][-1], equal_to(844))

    def testTargetOptimalSolution(self):
        solution, _, _ = self._numbers.lookup(175, [100, 75, 50, 25, 10, 8])
        assert_that(len(solution), equal_to(1))

    def testApproxSolution(self):
        solution, _, _ = self._numbers.lookup(844, [3, 5, 4, 3, 2, 1])
        assert_that(solution[-1][-1], equal_to(540))
        assert_that(len(solution), equal_to(5))


class testNumbersService(unittest.TestCase):
    def setUp(self):
        self._service = NumberService()

    def testEmptyParameters(self):
        try:
            self._service.solve(None, None)
        except ServiceException as f:
            assert_that(
                equal_to(f.errorcode == ServiceCodes.EMPTY_PARAMS))

    def testBadParameters(self):
        try:
            self._service.solve('house', [])
        except ServiceException as f:
            assert_that(
                equal_to(f.errorcode == ServiceCodes.BAD_PARAMS))

    def testBadTarget(self):
        try:
            self._service.solve(1000, [])
        except ServiceException as f:
            assert_that(
                equal_to(f.errorcode == ServiceCodes.BAD_PARAMS))

    def testBadNumbers(self):
        try:
            self._service.solve(999, [])
        except ServiceException as f:
            assert_that(
                equal_to(f.errorcode == ServiceCodes.FAIL))

    def testOK(self):
        solution, recur, exec_time = self._service.solve(999, [10] * 6)
        assert_that(len(solution), greater_than(0))
