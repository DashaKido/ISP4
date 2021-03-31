from serializer import *
from .sample_objects import *
import unittest

class TestSerializer(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.serializers = []
        for s in SERIALIZERS:
            self.serializers.append(create_serializer(s))

    """
    Tests empty dictionary, set, tuple, list
    """
    def test_empty_object(self):
        objects = [{}, set(), tuple(), []]

        for serializer in self.serializers:
            for obj in objects:
                with self.subTest(str(serializer) + ' : ' + str(obj)):
                    new_obj = serializer.loads(serializer.dumps(obj))

                    self.assertEqual(new_obj, obj)
    
    """
    Tests all supported simple types
    """
    def test_simple_types(self):
        items = [-666.666, 'HELLO', True, False, None]

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                for item in items:
                    obj = item
                    new_obj = serializer.loads(serializer.dumps(obj))
                    self.assertEqual(new_obj, obj)
                    self.assertEqual(type(new_obj), type(obj))

    """
    Tests all basic types, lists, lambdas, functions, classes, methods
    """
    def test_class_A_and_B(self):
        obj = A('name')

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_obj = serializer.loads(serializer.dumps(obj))
                
                self.compare_class_A(new_obj, obj)

    """
    Tests class and creating instance from it
    """
    def test_MyType(self):
        obj = MyType(54)

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_type = serializer.loads(serializer.dumps(MyType))

                new_obj = new_type(54)

                self.compare_class_MyType(new_obj, obj)        

    """
    Tests single function
    """
    def test_function(self):
        with self.subTest('recursive_fib_test'):
            for serializer in self.serializers:
                with self.subTest(str(serializer)):
                    func = serializer.loads(serializer.dumps(recursive_fib))
                
                    self.assertEqual(func(4), recursive_fib(4))
                    self.assertEqual(func(5), recursive_fib(5))
                    self.assertEqual(func(8), recursive_fib(8))

        with self.subTest('local function test'):
            for serializer in self.serializers:
                with self.subTest(str(serializer)):
                    func = serializer.loads(serializer.dumps(local_func_and_lambda))

                    self.assertEqual(func(555), local_func_and_lambda(555))
                    self.assertEqual(func(999), local_func_and_lambda(999))
                    self.assertEqual(func(123123), local_func_and_lambda(123123))

    """
    Tests dictionary
    """
    def test_dicts(self):
        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                d = serializer.loads(serializer.dumps(sample_dict))

                self.compare_sample_dicts(d, sample_dict)        

    """
    Tests class with static members
    """
    def test_static_members(self):
        obj = B()
        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_type = serializer.loads(serializer.dumps(B))

                new_obj = B()

                self.compare_class_B(new_obj, obj)

                self.assertEqual(new_type.a, B.a)
                self.assertEqual(new_type.b, B.b)
                self.assertEqual(new_type.c(123), B.c(123))
                self.assertEqual(new_type.b_func(), B.b_func())
    
    """
    Tests nested list
    """
    def test_nested_list(self):
        obj = sample_list

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_obj = serializer.loads(serializer.dumps(obj))

                self.compare_sample_lists(new_obj, obj)

    """
    Tests set with nested tuple
    """
    def test_set(self):
        obj = sample_set

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_obj = serializer.loads(serializer.dumps(obj))

                self.assertEqual(new_obj, obj)

    """
    Tests tuple with nested types of all supported formats
    """
    def test_tuple(self):
        obj = sample_tuple

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_obj = serializer.loads(serializer.dumps(obj))

                self.compare_sample_tuples(new_obj, obj)

    """
    Tests list and dict recursion
    """
    def test_list_and_dict_recursion(self):
        tests = test_recursion

        for serializer in self.serializers:
            for obj in tests:
                with self.subTest(str(serializer) + ' [' + str(tests.index(obj)) + ']'):
                    new_obj = serializer.loads(serializer.dumps(obj))

                    self.assertEqual(new_obj, obj)

    """
    Tests dump and load methods
    """
    def test_file(self):
        obj = A('Some Name')

        file_name = 'tests/test_file.txt'
        
        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                with open(file_name, 'w+') as fp:
                    serializer.dump(obj, fp)
                    new_obj = serializer.load(fp)
                    self.compare_class_A(new_obj, obj)

    """
    Tests simple dicts with tuple keys
    """
    def test_simple_dict_with_tuple_keys(self):
        tests = tuple_key_tests

        for serializer in self.serializers:
            for obj in tests:
                with self.subTest(str(serializer) + ' [' + str(tests.index(obj)) + ']'):
                    new_obj = serializer.loads(serializer.dumps(obj))

                    self.assertEqual(new_obj, obj)

    """
    Tests dict with tuple keys
    """
    def test_dict_with_tuple_keys(self):
        obj = dict_with_tuple_key

        for serializer in self.serializers:
            with self.subTest(str(serializer)):
                new_obj = serializer.loads(serializer.dumps(obj))

                self.assertEqual(new_obj, obj)

    def compare_sample_lists(self, new_obj, obj):
        self.assertEqual(new_obj[0], obj[0])
        self.assertEqual(new_obj[1], obj[1])
        self.assertEqual(new_obj[2], obj[2])

        self.assertEqual(new_obj[3][0](452), obj[3][0](452))
        self.assertEqual(new_obj[3][0](-12), obj[3][0](-12))
        self.assertEqual(new_obj[3][0](72), obj[3][0](72))

        self.assertEqual(new_obj[3][1](9), obj[3][1](9))
        self.assertEqual(new_obj[3][1](12), obj[3][1](12))

        self.compare_class_A(new_obj[3][2][0], obj[3][2][0])
        self.compare_class_B(new_obj[3][2][1], obj[3][2][1])
        self.compare_class_MyType(new_obj[3][2][2], obj[3][2][2])

        self.assertEqual(new_obj[3][2][3], obj[3][2][3])
    
    def compare_sample_dicts(self, d, sample_dict):
        self.assertEqual(d[1], sample_dict[1])
        self.assertEqual(d['b'][1]['a'], sample_dict['b'][1]['a'])
        self.assertEqual(d['b']['array'][0], sample_dict['b']['array'][0])
        self.assertEqual(d['b']['array'][1], sample_dict['b']['array'][1])
        self.assertEqual(d['b']['array'][2](0.53), sample_dict['b']['array'][2](0.53))

        new_obj = d[2]
        obj = sample_dict[2]

        self.compare_class_A(new_obj, obj)

        new_type = d['b']['type']

        new_obj = new_type()
        obj = B()

        self.compare_class_B(new_obj, obj)

    def compare_sample_tuples(self, new_obj, obj):
        self.assertEqual(new_obj[0], obj[0])
        self.assertEqual(new_obj[1], obj[1])
        self.assertEqual(new_obj[2], obj[2])

        self.compare_sample_dicts(new_obj[3], obj[3])
        self.compare_sample_lists(new_obj[4][0], obj[4][0])
        self.assertEqual(new_obj[4][1], obj[4][1])

    def compare_class_A(self, new_obj, obj):
        self.assertEqual(new_obj.name, obj.name)
        
        self.assertEqual(new_obj.arr[0], obj.arr[0])
        self.assertEqual(new_obj.arr[1], obj.arr[1])

        self.assertEqual(new_obj.arr[2](123,'qwe', 1, 2, 'qq'), 
                        obj.arr[2](123,'qwe', 1, 2, 'qq'))
        
        self.compare_class_B(new_obj.arr[3], obj.arr[3])

        self.assertEqual(new_obj.a, obj.a)
        self.assertEqual(new_obj.b, obj.b)
        self.assertEqual(new_obj.c, obj.c)
        self.assertEqual(new_obj.d, obj.d)
        self.assertEqual(new_obj.e, obj.e)
        self.assertEqual(new_obj.none, obj.none)
        self.assertEqual(new_obj.l(123), obj.l(123))
        self.assertEqual(new_obj.func('aaa'), obj.func('aaa'))

        self.assertEqual(new_obj.get_name(), obj.get_name())
        self.assertEqual(new_obj.set_name('ggg'), obj.set_name('ggg'))
        self.assertEqual(new_obj.get_name(), obj.get_name())

        self.assertEqual(new_obj.dict[1], obj.dict[1])
        self.assertEqual(new_obj.dict[2], obj.dict[2])
        self.assertEqual(new_obj.dict[3], obj.dict[3])

        self.assertEqual(new_obj.dict[4](5), obj.dict[4](5))
        self.assertEqual(new_obj.dict[4](10), obj.dict[4](10))
        
        self.compare_class_B(new_obj.dict[5](), obj.dict[5]())

        self.assertEqual(new_obj.dict[6][5][7], obj.dict[6][5][7])  

        self.assertEqual(new_obj.__class__.__name__, obj.__class__.__name__)

        self.assertEqual(new_obj.set, obj.set)
        self.assertEqual(new_obj.tuple, obj.tuple)

    def compare_class_B(self, new_obj, obj):
        self.assertEqual(new_obj.a, obj.a)
        self.assertEqual(new_obj.b, obj.b)
        self.assertEqual(new_obj.c('hello'), obj.c('hello'))
        self.assertEqual(new_obj.b_func(), obj.b_func())

        self.assertEqual(new_obj.__class__.__name__, obj.__class__.__name__)

    def compare_class_MyType(self, new_obj, obj):
        self.assertEqual(new_obj.get_age(), obj.get_age())
        self.assertEqual(new_obj.get_str_age(), obj.get_str_age())
        
        self.assertEqual(new_obj.class_var, obj.class_var)
        self.assertEqual(new_obj.class_var, obj.class_var)

        self.assertEqual(new_obj.__class__.__name__, obj.__class__.__name__)
