_solvers = dict()


def register(*, day):
    def decorator(fn):
        _solvers[day] = fn
        return fn
    return decorator


def get_solver(day):
    return _solvers[day]
