class Field():
    def __init__(self):
        raise NotImplementedError('Not implemented')

    def __get__(self, instance, owner):
        raise NotImplementedError('Not implemented')

    def __set__(self, instance, value):
        raise NotImplementedError('Not implemented')

class StringField(Field):
    def __init__(self):
        self.__type = str
        self.__value = str()
        self.name = None
    def __get__(self, instance, owner):
        return getattr(instance, self.name, str())
    def __set__(self, instance, value):
        try:
            if type(value) != str:
                raise Exception()
            setattr(instance, self.name, value)
        except:
            print(f'ERROR: instance: {instance}; name: {self.name}; invalid value: {value}')

class IntField(Field):
    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        try:
            if type(value) != int:
                raise Exception()
            setattr(instance, self.name, value)
        except:
            print(f'ERROR: instance: {instance}; name: {self.name}; invalid value: {value}')


class ModelCreator(type):
    def __new__(cls, name, bases, namespace):
        storage = set()

        for base in bases:
            if hasattr(base, '__slots__'):
                storage.update(base.__slots__)

        for k, v in namespace.items():
            if isinstance(v, Field):
                v.name = "_{}".format(k)
                storage.add(v.name)

        def __new__(cls, *args, **kwargs):
            instance = object.__new__(cls)
            for k, v in kwargs.items():
                if '_{}'.format(k) in cls.__slots__:
                    setattr(instance, k, v)
            return instance
        namespace['__new__'] = __new__
        namespace['__slots__'] = list(storage)
        new_cls = super(ModelCreator, cls).__new__(cls, name, bases, namespace)
        return new_cls

class Student(metaclass=ModelCreator):
    name = StringField()
    age = IntField()

s = Student(name='hi',age = 20)
print(s.name)
print(s.age)