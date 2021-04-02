def fib(n):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
        yield a
        
for i in fib(123):
    print(i)
