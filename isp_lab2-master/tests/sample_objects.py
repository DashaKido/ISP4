"""
simple function for tests
"""
def f(a, b = 'default', *args):
    local_var = a * 3
    return str(local_var) + b + str(len(args))

"""
class for static methods testing
"""
class B:
    a = 666
    b = [333, 666, 'www']

    @staticmethod
    def c(n):
        return str(n) + '!!!'
    
    @staticmethod
    def b_func():
        return 'Hello from B class method'

"""
class for testing all supported types
"""
class A:
    def __init__(self, name):
        self.none = None
        self.name = name
        self.arr = [1, "some string", f, B]
        self.a = 1
        self.b = -123.123
        self.c = "abacaba"
        self.d = True
        self.e = False

        self.set = {1, 'qwe', 'rty', False, True, None, (-123.1, False)}
        self.tuple = ('qwe', 'rty', 6666666, {1, 2, 3, False, ('haha', 'nooo', 7777, -131.31313), True, None})
        self.dict = {1: 1, 2: 4, 3: 9, 4: recursive_fib, 5: B, 6: {5 : {7: [1, 2, 3]}}}

        self.l = lambda x: x ** 2
        self.func = f       

    def get_name(self):
        return self.name

    def set_name(self, string):
        self.name = string

"""
class for class serializing tests
"""
class MyType:
    def __init__(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def get_str_age(self):
        return 'Your age is ' + str(self.get_age())

    @staticmethod
    def say_hello():
        return 'hello'

    class_var = 123

"""
recursive function for tests
"""
def recursive_fib(n):
    if n < 2:
        return 1

    return recursive_fib(n - 1) + recursive_fib(n - 2)

"""
function with local function and lambda for tests
"""
def local_func_and_lambda(n):
    def h(n):
        return n ** 2

    l = lambda n: n ** 0.5

    return l(h(n) + h(n))

sample_dict = {1: 'qwe', 
               'a': f, 
               2: A('name'), 
               'b': {
                        1 : {'a': 'hello'}, 
                        'array': [1, 'gg', local_func_and_lambda],
                        'type': B
                    }
               }

sample_list = [1, 2, 'a', 
                    [local_func_and_lambda, recursive_fib, 
                        [A('nested list'), B(), MyType(19), 
                            [None, True, False]]]]

sample_set = {'qwe', 1, -1, 0.1, 10e10, ('qwe', None, (1, 2, 'wwww')), False, True}

funny_tuple = ((((((((('qweqwe',),),),),),),),), 1)

"""
Tuple of all previous sample objects
"""
sample_tuple = (1, 'F', funny_tuple, sample_dict, (sample_list, sample_set))


"""
Objects for testing recursion
"""
recursion_a = {'a': 1, 'b': {'a': False, 'n': True, 1: None, 'm': 
                {'l': [], 'v': 'nooo', 'n': {}}}, 'o': 123.12, 'f': tuple(), 'g': set()}

recursion_b = {'a': [1, 2, 3, [], []]}

recursion_c = [1, 2, 3, {'a': {}}]

recursion_d = [1, {'a': [4, {'b': False}, 5]}, 1]

recursion_e = [1, 2, {'a': [1, 2, 3], 'b': [4, 'qwe', None]}, {'b': {'a': 'hello'}}]

recursion_f = []

recursion_g = {'a': 
        {'c':'qwe', 
         'g': {'l': [1, {'a' : 'hello', 'b': 'hi'}, 3]}
        }, 
    'b': 
        {'f': [1, 2, 3],
         'b': False,
         'c': True,
         'n': None
        }
    }

recursion_h = [[1, 2, 3], [1, [2,[4, [5], 6]]], [7, 8, [9]]]

recursion_i = [{'a': 123, 'b': 666}, 'qwe', False, True, ['hello', None]]

test_recursion = [recursion_a,
                  recursion_b,
                  recursion_c,
                  recursion_d,
                  recursion_e,
                  recursion_f,
                  recursion_g,
                  recursion_h,
                  recursion_i]

"""
Dictionary with tuple keys
"""
dict_with_tuple_key = {(): 1, 
                       (3, ((4.1, False), (None, 'qwe'))): 
                            {
                                (1, 2): ('qwe', 'rty'),
                                ('hello', True): recursion_g,
                                0: 5,
                                ((1,),(1,)): recursion_a
                            }
                        }

"""
Simple cases of tuple keys
"""
tuple_key_a = {(1, 2): [3, 4]}

tuple_key_b = {(False, None): (3, 4)}

tuple_key_c = {(1, 'qwe'): 3}

tuple_key_d = {(1, 2): {3, 4}}

tuple_key_e = {(1, 2): {(3, 4): {(5, 6): 7}}}

tuple_key_f = {(1, 2): {(3, 4): (5, 6)}}

tuple_key_g = (1, (2, 3))

tuple_key_h = {(1, 2): {(2, 3): 4}}

tuple_key_i = {(1, 2): {(3, 4): {'a': 1}}}

tuple_key_tests = [tuple_key_a,
                   tuple_key_b,
                   tuple_key_c,
                   tuple_key_d,
                   tuple_key_e,
                   tuple_key_f,
                   tuple_key_g,
                   tuple_key_h,
                   tuple_key_i]