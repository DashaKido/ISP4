class Field():
    def __init__(self):
        raise NotImplementedError('Not implemented')

    def __get__(self, instance, owner):
        raise NotImplementedError('Not implemented')

    def __set__(self, instance, value):
        raise NotImplementedError('Not implemented')

class StringField(Field):
    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

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
    def __new__(cls, name, bases, attrs):
        storage = set()

        for base in bases:
            if hasattr(base, '__slots__'):
                storage.update(base.__slots__)
        
        for k, v in attrs.items():
            if isinstance(v, Field):
                v.name = f'_{k}'
                storage.add(v.name)

        def __new__(cls, **kwargs):
            instance = object.__new__(cls)

            for k, v in kwargs.items():
                if f'_{k}' in cls.__slots__:
                    setattr(instance, k, v)
            
            return instance
        
        attrs['__new__'] = __new__
        attrs['__slots__'] = list(storage)

        new_cls = super().__new__(cls, name, bases, attrs)
        return new_cls

class Person(metaclass=ModelCreator):
    age = IntField()
    name = StringField()

s = Person(name = 'qweqwe', age = 123)

print(s.name)
print(s.age)
