class Seq:
    def __init__(self, iterable):
        self.iterable = list(iterable)

    def __iter__(self):
        return self.iterable.__iter__()

    def __next__(self):
        return self.iterable.__next__()

    def filter(self, cond):
        res = list()
        for obj in self:
            if cond(obj):
                res.append(obj)
        return type(self)(res)

l = [2, - 1, 3, 0, -5, 10]

a = Seq(l)

for i in a:
    print(i, end=' ')

print()
for i in a.filter(lambda x: x <= 0):
    print(i, end=' ')

print()
for i in a.filter(lambda x: x & 1 == 0):
    print(i, end=' ')
