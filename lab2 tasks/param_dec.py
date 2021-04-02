def param_dec(dec):
    def new_dec(*args, **kwargs):
        print(*args, **kwargs)
        return dec
        # def wrapper(f):
        #     print('new_dec wrapper')
        #     print(*args, **kwargs)
        #     return dec(f)
        # return wrapper
    return new_dec

@param_dec
def say_hi(f):
    def wrapper(*args, **kwargs):
        print('old wrapper')
        return f(*args, **kwargs)
    return wrapper

# def say_hi(*args, **kwargs):
#     def decorator(f):
#         print(*args, **kwargs)
#         def wrapper(*args, **kwargs):
#             print('wrapper')
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator

@say_hi('some params')
def sum(a, b):
    return a + b

print(sum(1, 5))