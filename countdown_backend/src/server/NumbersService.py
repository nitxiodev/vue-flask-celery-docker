from countdown_backend.src.numbers_solver.numbers_backtracking import NumbersSolver
from countdown_backend.src.server import ServiceException, ServiceCodes


class NumberService(object):
    def __init__(self):
        self._solver = NumbersSolver()

    def solve(self, target, numbers):
        if target is None or numbers is None:
            raise ServiceException(ServiceCodes.EMPTY_PARAMS, msg='Empty parameters')

        try:
            target = int(target)
        except (TypeError, ValueError) as f:
            raise ServiceException(ServiceCodes.BAD_PARAMS, msg=f.message)

        # Target is only allowed in the range [100, 999]
        if target < 100 or target > 999:
            raise ServiceException(ServiceCodes.BAD_PARAMS, msg='Bad target. Must be between [100, 999]')

        try:
            return self._solver.lookup(target, numbers)
        except TypeError as f:
            raise ServiceException(ServiceCodes.FAIL, msg=f.message)
