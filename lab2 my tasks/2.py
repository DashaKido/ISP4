#гениратор чисел Фибоначчи
def fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a+b

gen = fib()
for i in range(10):
    print(next(gen))