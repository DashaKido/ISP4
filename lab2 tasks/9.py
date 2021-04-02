class MyRange:
    def __init__(self, *args):
        if len(args) == 1:
            self.stop = args[0]
            self.start = 0
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
        elif len(args) == 3:
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
        else:
            raise Exception('invalid range')

    def __iter__(self):
        return self

    def __next__(self):
        a = self.start
        self.start += self.step

        if a >= self.stop:
            raise StopIteration('iteration finished')

        return a

for i in MyRange(50, 100, 3):
    print(i, end=' ')