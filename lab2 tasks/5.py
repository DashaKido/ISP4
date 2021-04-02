class MetaLogger(type):
    _logs = {}

    def __new__(cls, name, bases, attrs):
        if name not in cls._logs.keys():
            cls._logs[name] = f'Logs of class "{name}":\n\n'

        for k in attrs.keys():
            if callable(attrs[k]):
                attrs[k] = cls.logger(cls, name, attrs[k])

        def __str__(self):
            if isinstance(self, type):
                return cls.get_log(self.__name__)
            return cls.get_log(self.__class__.__name__)

        attrs['__str__'] = __str__

        return super().__new__(cls, name, bases, attrs)
    
    def logger(cls, name, f):
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            cls._logs[name] += f'function name: {f.__name__}\nargs: {args}\nkwargs: {kwargs}\nreturns: {res}\n\n'
            return res
        return wrapper
    
    def get_log(name):
        if name in MetaLogger._logs.keys():
            return MetaLogger._logs[name]
        return 'No logs :('

    def __str__(self):
        if isinstance(self, type):
            return MetaLogger.get_log(self.__name__)
        return MetaLogger.get_log(self.__class__.__name__)

class Logger(metaclass = MetaLogger):
    pass


class A(Logger):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def func(self, a, b):
        return str(self.name) + str(a) + str(b)

a = A('qwe')

a.get_name()

a.func(b = False, a = 123)

print(str(a))

print(type([]))
