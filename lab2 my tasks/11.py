class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Logger(metaclass=MetaSingleton):
    pass

obj1 = Logger()
obj2 = Logger()
print(obj1)
print(obj2)
