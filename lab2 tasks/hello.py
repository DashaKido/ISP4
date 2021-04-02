class Meta(type):
    def __new__(cls, name, bases, attrs):
        print(attrs)
        return super().__new__(cls, name, bases, attrs)

class A(object, metaclass = Meta):
    pass

a = A()