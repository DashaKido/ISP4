import serializer
import inspect
import os
obj = {"foo":{"bar":[1,2,3]}}
new_obj = serializer.JsonSer.loads(serializer.JsonSer.dumps(obj))
print(new_obj)

obj = {'a': 1,
            'b': 'some',
            'c': 2.2,
            'd': {
                'a': 1,
                'b': [True, None, False]
                },
            'e': (1, 2.2, 3.3)
            }

file_name = 'file.json'
with open(file_name, 'w+') as fp:
    serializer.JsonSer.dump(obj, fp)
    new_obj = serializer.JsonSer.load(fp)
print((lambda x: x + 1)(15))
new_obj = serializer.LambdaPars.to_str(serializer.LambdaPars.parse_lambda((lambda x: x + 1)))
f = eval(new_obj)
print(f(15))

A = "hi"
obj = serializer.JsonSer.getFromGlobal(A)
print(obj)