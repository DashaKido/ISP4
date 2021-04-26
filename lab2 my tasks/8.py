def cached(func):
    if not hasattr(func, 'cache'):
        func.cache = {}
        # позиционное количество аргументов
        # позиционное количество именованных аргументов
    def wrapper(*args, **kwargs):
        print(f'\nPrev cache: {func.cache}')

        cur_params = (args, tuple(kwargs.items()))

        if cur_params not in func.cache:
            res = func(*args, **kwargs)
            func.cache[cur_params] = res
            print(f'Updated cache: {func.cache}')
            return res
        else:
            return func.cache[cur_params]
    return wrapper

@cached
def sqr(x):
    return x*x

print(sqr(5))
print(sqr(123))
print(sqr(x=5))
print()
print(sqr(5))
print(sqr(123))
print(sqr(x=5))
