class Meta(type):
    d = {'a': 1, 'b': 2, 'c': None, 'd': { False: True }}
    
    def __new__(cls, name, bases, attrs):
        attrs.update(Meta.d)
        return super().__new__(cls, name, bases, attrs)

class A(metaclass = Meta):
    def __init__(self, name):
        self.name = name

a = A('qwe')

print(a.a)
print(a.b)
print(a.c)
print(a.d)
print(a.name)

print()

print(A.a)
print(A.b)
print(A.c)
print(A.d)