#класс n-мерный вектор
class Vector():
    def __init__(self, list_ = []):
        self._vector = list_

    def __str__(self):
        return str(self._vector)

    def append(self, a):
        self._vector.append(a)

    def __add__(self, other):
        res = self._vector
        for i in range(len(self._vector)):
            res[i] += other._vector[i]
        return  res
    
    def __sub__(self, other):
        res = self._vector
        for i in range(len(self._vector)):
            res[i] -= other._vector[i]
        return  res
    
    def __mul__(self, other):
        res = self._vector
        for i in range(len(self._vector)):
            res[i] *= other._vector[i]
        return  res

a = Vector([1, 2, 3])
b = Vector([4, 2, 1])

print(a * b)