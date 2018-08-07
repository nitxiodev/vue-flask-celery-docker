from datetime import datetime
from itertools import permutations


class NumbersSolver(object):
    def __init__(self):
        self._ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if (x % y) == 0 else 0
        }

    def lookup(self, target, numbers):
        approx_solution = {0: 10e6, 'sol': []}
        memoization = {'rec': 0}

        init_time = datetime.now()
        current_solution = self._inner_lookup(0, target, approx_solution, permutations(sorted(numbers), 2),
                                              sorted(numbers), [], [], memoization)
        ellapsed_time = (datetime.now() - init_time).total_seconds()
        output = current_solution or approx_solution['sol']

        return output, memoization['rec'], ellapsed_time

    def _inner_lookup(self, partial_target, target, approx, numbers, numbers_list, solution, best, memoization):
        if partial_target == target:
            return solution
        else:
            for comb in numbers:
                for op in self._ops:
                    x, y = comb
                    result = self._ops[op](x, y)
                    if result > 0 and result != x and result != y:
                        new_numbers = numbers_list[:]
                        new_numbers.remove(x)
                        new_numbers.remove(y)
                        new_numbers = sorted(new_numbers + [result])

                        if not memoization.get(str(new_numbers)):  # Memoization
                            memoization[str(new_numbers)] = True
                            new_sol = solution + [[max(x, y), op, min(x, y), result]]

                            # The nearest result to target
                            if (result - target) ** 2 < approx[0] ** 2:
                                approx[0] = result - target
                                approx['sol'] = new_sol

                            if (not best or len(best) > len(new_sol)) and len(new_numbers) > 1:
                                memoization['rec'] += 1
                                sol = self._inner_lookup(result, target, approx, permutations(new_numbers, 2),
                                                         new_numbers, new_sol, best, memoization)

                                if sol:
                                    best = sol[:]

        return best
