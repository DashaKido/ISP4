import unittest
import serializer
from .tests_objects import *

class TestStringMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestStringMethods, self).__init__(*args, **kwargs)
        serializer.create_serializer('JSON')

    def test_empty_object(self):
        obj = {}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_basic_object(self):
        obj = {"foo":"bar"}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_basic_number(self):
        obj = {"foo":1}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_empty_array(self):
        obj = {"foo":[]}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_basic_array(self):
        obj = {"foo":[1,2,"three"]}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_nested_object(self):
        obj = {"foo":{"bar":2}}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_true(self):
        obj = {"foo":True}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_false(self):
        obj = {"foo":False}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_null(self):
        obj = {"foo":None}
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_basic_whitespace(self):
        obj = { "foo" : [1, 2, "three"] }
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)

    def test_dict(self):
        obj = some_dict
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj['a'], obj['a'])
        self.assertEqual(new_obj['d']['a'], obj['d']['a'])

    def test_list(self):
        obj = some_list
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj[1], obj[1])
        self.assertEqual(new_obj[2][1], obj[2][1])
    
    def test_set(self):
        obj = some_set
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj, obj)
    
    def test_tuple(self):
        obj = some_tuple
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj[0], obj[0])
        self.assertEqual(new_obj[1], obj[1])
        self.assertEqual(new_obj[3][1][1], obj[3][1][1])

    def test_file_dict(self):
        obj = some_dict
        file_name = 'tests/test.txt'
        with open(file_name, 'w+') as fp:
            serializer.JsonSer.dump(obj, fp)
            new_obj = serializer.JsonSer.load(fp)
            self.assertEqual(new_obj['a'], obj['a'])
            self.assertEqual(new_obj['d']['a'], obj['d']['a'])
    
    def test_file_list(self):
        obj = some_list
        file_name = 'tests/test.txt'
        with open(file_name, 'w+') as fp:
            serializer.JsonSer.dump(obj, fp)
            new_obj = serializer.JsonSer.load(fp)
            self.assertEqual(new_obj[1], obj[1])
            self.assertEqual(new_obj[2][1], obj[2][1])
    
    def test_file_set(self):
        obj = some_set
        file_name = 'tests/test.txt'
        with open(file_name, 'w+') as fp:
            serializer.JsonSer.dump(obj, fp)
            new_obj = serializer.JsonSer.load(fp)
            self.assertEqual(new_obj, obj)
    
    def test_func(self):
        obj = some_func
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj(5), obj(5))
        self.assertEqual(new_obj(100), obj(100))
        self.assertEqual(new_obj(300), obj(300))
    
    def test_func_lambda(self):
        obj = some_func_lambda
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj(5), obj(5))
        self.assertEqual(new_obj(100), obj(100))
        self.assertEqual(new_obj(300), obj(300))
    
    def test_static_class(self):
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(Some))
        self.assertEqual(new_obj.some, Some.some)
        self.assertEqual(new_obj.arg, Some.arg)
        self.assertEqual(new_obj.arr, Some.arr)
        self.assertEqual(new_obj.static_m(1), Some.static_m(1))
    
    def test_class(self):
        obj = Another('arg')
        new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
        self.assertEqual(new_obj.arg, obj.arg)
        self.assertEqual(new_obj.tr, obj.tr)
        self.assertEqual(new_obj.arr, obj.arr)
        self.assertEqual(new_obj.int, obj.int)
        self.assertEqual(new_obj.float, obj.float)    
        self.assertEqual(new_obj.dict['a'], obj.dict['a'])
        self.assertEqual(new_obj.dict['d']['a'], obj.dict['d']['a'])
        self.assertEqual(new_obj.set, obj.set)  
        self.assertEqual(new_obj.get_arg(), obj.get_arg())  
        self.assertEqual(new_obj.set_arg('hi'), obj.set_arg('hi'))  
        self.assertEqual(new_obj.get_arg(), obj.get_arg())

    def test_file_static_class(self):
        obj = Some
        file_name = 'tests/test.txt'
        with open(file_name, 'w+') as fp:
            serializer.JsonSer.dump(obj, fp)
            new_obj = serializer.JsonSer.load(fp)
            self.assertEqual(new_obj.some, obj.some)
            self.assertEqual(new_obj.arg, obj.arg)
            self.assertEqual(new_obj.arr, obj.arr)
            self.assertEqual(new_obj.static_m(1), obj.static_m(1))

    @staticmethod
    def parse_to_str(f):
        return serializer.LambdaPars.to_str(serializer.LambdaPars.parse_lambda(f))

    def test_l_binary(self):
        self.assertEqual('lambda x: x + 1', self.parse_to_str(lambda x: x + 1))
        self.assertEqual('lambda x: x + 1 + a', self.parse_to_str(lambda x: x + 1 + a))
        self.assertEqual('lambda x: x + 1 + a', self.parse_to_str(lambda x: (x + 1) + a))
        self.assertEqual('lambda x: x + (1 + a)', self.parse_to_str(lambda x: x + (1 + a)))
        self.assertEqual('lambda x: (x + 1) * a', self.parse_to_str(lambda x: (x + 1) * a))
        self.assertEqual('lambda: a ** b ** c', self.parse_to_str(lambda: a ** b ** c))
        self.assertEqual('lambda: a ** b ** c', self.parse_to_str(lambda: a ** (b ** c)))
        self.assertEqual('lambda: (a ** b) ** c', self.parse_to_str(lambda: (a ** b) ** c))

    def test_l_and_or(self):
        self.assertEqual('lambda: a and b', self.parse_to_str(lambda: a and b))
        self.assertEqual('lambda: a or b', self.parse_to_str(lambda: a or b))
        self.assertEqual('lambda: a and b and c', self.parse_to_str(lambda: a and b and c))
        self.assertEqual('lambda: a or b or c', self.parse_to_str(lambda: a or b or c))
        self.assertEqual('lambda: a and b or c', self.parse_to_str(lambda: a and b or c))
        self.assertEqual('lambda: a or b and c', self.parse_to_str(lambda: a or b and c))
        self.assertEqual('lambda: a and (b or c)', self.parse_to_str(lambda: a and (b or c)))
        self.assertEqual('lambda: (a or b) and c', self.parse_to_str(lambda: (a or b) and c))
        self.assertEqual('lambda: (a and b) + 1', self.parse_to_str(lambda: (a and b) + 1))

    def test_l_if_else(self):
        self.assertEqual('lambda: a if b else c', self.parse_to_str(lambda: a if b else c))
        self.assertEqual('lambda: a if not b else c', self.parse_to_str(lambda: a if not b else c))
        self.assertEqual('lambda: a if b else c if d else e', self.parse_to_str(lambda: a if b else c if d else e))
        self.assertEqual('lambda: a if b else c if d else e', self.parse_to_str(lambda: a if b else (c if d else e)))

    def test_l_build_literal(self):
        self.assertEqual('lambda: 1', self.parse_to_str(lambda: 1))
        self.assertEqual('lambda: [1, 2, 3]', self.parse_to_str(lambda: [1, 2, 3]))
        self.assertEqual('lambda: []', self.parse_to_str(lambda: []))
        self.assertEqual('lambda: (1, 2, 3)', self.parse_to_str(lambda: (1, 2, 3)))
        self.assertEqual('lambda: (1,)', self.parse_to_str(lambda: (1,)))
        self.assertEqual('lambda: ()', self.parse_to_str(lambda: ()))
        self.assertEqual('lambda: {1, 2, 3}', self.parse_to_str(lambda: {1, 2, 3}))
        self.assertEqual('lambda: {}', self.parse_to_str(lambda: {}))
        self.assertEqual('lambda: {a: 1, b: 2}', self.parse_to_str(lambda: {a: 1, b: 2}))
        self.assertEqual('lambda: {a: 1, b: 2, c: 3}', self.parse_to_str(lambda: {a: 1, b: 2, c: 3}))

    def test_l_attr_subscr(self):
        self.assertEqual('lambda: a.b', self.parse_to_str(lambda: a.b))
        self.assertEqual('lambda: a.b.c', self.parse_to_str(lambda: a.b.c))
        self.assertEqual('lambda: a.b.c', self.parse_to_str(lambda: (a.b).c))
        self.assertEqual('lambda: a[b]', self.parse_to_str(lambda: a[b]))
        self.assertEqual('lambda: a[b].c', self.parse_to_str(lambda: a[b].c))
        self.assertEqual('lambda: a.b[c]', self.parse_to_str(lambda: a.b[c]))

    def test_l_simple_call(self):
        self.assertEqual('lambda x: f(x)', self.parse_to_str(lambda x: f(x)))
        self.assertEqual('lambda x: f(x + 1) * 2', self.parse_to_str(lambda x: f(x + 1) * 2))
        
    def test_l_comparison(self):
        self.assertEqual('lambda: a < b', self.parse_to_str(lambda: a < b))
        self.assertEqual('lambda: a < b and b < c', self.parse_to_str(lambda: a < b and b < c))
        self.assertEqual('lambda: a < b and b < c', self.parse_to_str(lambda: a < b < c))
        self.assertEqual('lambda: (a < b and b < c) and d < e', self.parse_to_str(lambda: a < b < c and d < e))
        self.assertEqual('lambda: a < b and b < c and d < e', self.parse_to_str(lambda: a < b and b < c and d < e))
        self.assertEqual('lambda: a < b and b < c and d < e', self.parse_to_str(lambda: (a < b and b < c) and d < e))

    def test_lambda_in_lambda(self):
        self.assertEqual('lambda: lambda x: x', self.parse_to_str(lambda: lambda x: x))
        self.assertEqual('lambda x: lambda: x', self.parse_to_str(lambda x: lambda: x))

if __name__ == '__main__':
    unittest.main()
