class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
        
class A():
    def __call__(self):
        print('hi')

obj1 = A()
obj2 = A()

obj1()

print(obj1, obj2)
