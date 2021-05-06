some_dict = {'a': 1,
            'b': 'some',
            'c': 2.2,
            'd': {
                'a': 1,
                'b': [True, None, False]
                },
            'e': [1, 2.2, 3.3]
            }

some_list = [1, 2.2, 
                [True, None, False,
                            ['some', 'string']]]

some_set = {'some', 'string', 1, 2.2, (True,(False,(None, 2.2)))}

some_tuple = (1, 2.2, 'string', ('some',(True,(False,(None)))))

global_var = 1

def global_func(n):
    result = n + global_var
    return result

def some_func(a, b='hi'):
    res = a + 3
    return str(res) + b

def some_func_lambda(a):
    lambda a: a + 3
    return a

class Some:
    some = 1
    arg = 2.2
    arr = [True, 'some', 'string']
    @staticmethod
    def static_m(a):
        return str(a) + 'Hi'

class Another:
    def __init__(self, arg):
        self.tr = True
        self.arg = arg
        self.arr = [1, 2.2, 'string']
        self.int = 1
        self.float = 2.2
        self.dict = {'a': 1,
            'b': 'some',
            'c': 2.2,
            'd': {
                'a': 1,
                'b': [True, None, False]
                },
            'e': [1, 2.2, 3.3]
            }
        self.set  = {'some', 'string', 1, 2.2, (True,(False,(None, 2.2)))}
    
    def get_arg(self):
        return self.arg
    
    def set_arg(self, arg):
        self.arg = arg

