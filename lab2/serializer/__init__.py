from .lexer import lex
from .parser import parse
from .constants import *
from .converter import *
import inspect
import types
import re
import dis
_bin_prec = {
        'or': 5,
        'and': 7,
        'in': 10, 'is': 10, 'not in': 10, 'is not': 10,
        '<': 10, '<=': 10, '>': 10, '>=': 10, '==': 10, '!=': 10,
        '|': 12,
        '^': 14,
        '&': 16,
        '<<': 18, '>>': 18,
        '+': 20, '-': 20,
        '*': 22, '@': 22, '/': 22, '//': 22, '%': 22,
        '**': 27,
        '[]': 30,
    }
_un_prec = {
        'not': 11,
        '+': 25, '-': 25, '~': 25,
    }
_unary_lookup = {
        'UNARY_POSITIVE': '+',
        'UNARY_NEGATIVE': '-',
        'UNARY_NOT': 'not',
        'UNARY_INVERT': '~',
    }
_binary_lookup = {
        'BINARY_POWER': '**',
        'BINARY_MULTIPLY': '*',
        'BINARY_MATRIX_MULTIPLY': '@',
        'BINARY_FLOOR_DIVIDE': '//',
        'BINARY_TRUE_DIVIDE': '/',
        'BINARY_MODULO': '%',
        'BINARY_ADD': '+',
        'BINARY_SUBTRACT': '-',
        'BINARY_SUBSCR': '[]',
        'BINARY_LSHIFT': '<<',
        'BINARY_RSHIFT': '>>',
        'BINARY_AND': '&',
        'BINARY_XOR': '^',
        'BINARY_OR': '|',
    }
#функция для фабричного метода
def create_serializer(string):
    #проверка на соответствие строк
    if string == 'JSON':
        #вызываем наш класс
        return JsonSer()
    #или исключенеи
    raise Exception('Serializer was not created')
#класс сериализатор
class JsonSer:
    #из строки в обьект
    def loads(string):
        #вызываем лексический анализатор
        tokens = lex(string)
        #вызываем синтаксический анализатор
        result = parse(tokens)[0]
        #возвращаем результат
        return result
    #из обьекта в строку
    def dumps(obj, is_dict = True):
        #если обьект словарь
        if type(obj) == dict:
            string = ''
            #если верно
            if (is_dict):
                #прибавляем к строке флаг
                string += JSON_DICT_FLAG

            string += '{'
            dict_len = len(obj)

            if dict_len == 0:
                string += '}'
            #возвращаем пары(индексы и значения) из словаря(ключ и значение)
            for i, (key, val) in enumerate(obj.items()):
                #если ключ это строка
                if type(key) == str:
                    string += '"{}": {}'.format(key, JsonSer.dumps(val, type(val) == dict))
                elif type(key) == tuple:
                    string += '{}: {}'.format(JsonSer.dumps(key, type(key) == dict), 
                            JsonSer.dumps(val, type(val) == dict))
                else:
                    string += '{}: {}'.format(key, JsonSer.dumps(val, type(val) == dict))

                if i < dict_len - 1:
                    string += ', '
                else:
                    string += '}'
            #возвращаем полученную строку
            return string
        #если обьект список
        elif type(obj) == list:
            string = '['
            list_len = len(obj)

            if list_len == 0:
                return string + ']'
             #возвращаем пары(индексы и значения) из обьекта
            for i, val in enumerate(obj):
                string += JsonSer.dumps(val, type(val) == dict)

                if i < list_len - 1:
                    string += ', '
                else:
                    string += ']'

            return string 
        #если обьект можно вызвать или это класс
        elif callable(obj) or inspect.isclass(obj):
            #строка это возвращаемый исходный код обьекта в виде одной строки 
            #заменяем кавычки
            string = inspect.getsource(obj).replace('"', "'")
            return '"' + string + '"'
        elif type(obj) == str:
            return '"{}"'.format(obj)
        elif type(obj) == bool:
            return 'true' if obj else 'false'
        elif type(obj) == type(None):
            return 'null'
        #проверка на приметивные типы
        elif is_primitive(obj):
            return str(obj)
        #если обьект это кортеж
        if type(obj) == tuple:
            return JSON_TUPLE_FLAG + JsonSer.dumps(list(obj), False)
        #если обьект это множество
        if type(obj) == set:
            return JSON_SET_FLAG + JsonSer.dumps(list(obj), False)
        #если ничего не прошло то вызываем функцию 
        #преобразующую обьект в словарь
        return JsonSer.dumps(obj_to_dict(obj), False)
    #из файла в обьект
    def load(fp):
        #перемещаем указаль на начало файла
        fp.seek(0)
        #считываем и возвращаем все данные из файла
        string = fp.read()
        #вызываем метод из строки в обьект
        return JsonSer.loads(string)  
    #из обьекта в файл
    def dump(obj, fp):
        #вызываем метод из обьекта в строку
        string = JsonSer.dumps(obj)
        #записываем в файл данные
        fp.write(string)
        #сбрасываем данные из буфера файла
        fp.flush()
    #работа с глобальными переменными 
    def getFromGlobal(f):
        #создаем глоб переменную
        global some_var
        #задаем ей значение
        some_var = f
        ff = ''
        #возвращаем словарь с глобальной таблицей символов опредеделенных в модуле
        #при это м возвращаем пары(ключ, значение) для каждого элемента словаря
        for k,v in globals().items():
            #берем только значение и проверяем его с нашей переменной
            if v == some_var:
                ff = v
        #вызываем метод из обьекта в строку
        return JsonSer.dumps(ff)

class LambdaPars:

    def to_str(ex):
        if type(ex) is Lambda:
            if ex.args:
                return 'lambda {}: {}'.format(', '.join(ex.args),LambdaPars.to_str(ex.expr))
            return 'lambda: {}'.format(LambdaPars.to_str(ex.expr))
        if type(ex) is Val:
            return str(ex.v)
        if type(ex) in (Arg, Global):
            return str(ex.n)
        if type(ex) is Attr:
            p = LambdaPars._get_prec(ex)
            if p > LambdaPars._get_prec(ex.x):
                return '({}).{}'.format(LambdaPars.to_str(ex.x), ex.n)
            return '{}.{}'.format(LambdaPars.to_str(ex.x), ex.n)
        if type(ex) is BinOp:
            p = LambdaPars._get_prec(ex)
            if ex.op == '[]':
                if p > LambdaPars._get_prec(ex.x):
                    return '({})[{}]'.format(LambdaPars.to_str(ex.x), LambdaPars.to_str(ex.y))
                return '{}[{}]'.format(LambdaPars.to_str(ex.x), LambdaPars.to_str(ex.y))
            fx = '{}' if p <= LambdaPars._get_prec(ex.x)&62 else '({})'
            fy = '{}' if p|1 <= LambdaPars._get_prec(ex.y) else '({})'
            f = fx + ' {} ' + fy
            return f.format(LambdaPars.to_str(ex.x), ex.op, LambdaPars.to_str(ex.y))
        if type(ex) is UnOp:
            t = ex.op
            if t[-1].isalpha():
                t = t + ' '
            if LambdaPars._get_prec(ex) > LambdaPars._get_prec(ex.x):
                return '{}({})'.format(t, LambdaPars.to_str(ex.x))
            return '{}{}'.format(t, LambdaPars.to_str(ex.x))
        if type(ex) is Call:
            if LambdaPars._get_prec(ex) > LambdaPars._get_prec(ex.f):
                return '({})({})'.format(LambdaPars.to_str(ex.f), ', '.join(map(LambdaPars.to_str, ex.args)))
            return '{}({})'.format(LambdaPars.to_str(ex.f), ', '.join(map(LambdaPars.to_str, ex.args)))
        if type(ex) is IfElse:
            p = LambdaPars._get_prec(ex)
            fc = '{}' if p < LambdaPars._get_prec(ex.c) else '({})'
            ft = '{}' if p < LambdaPars._get_prec(ex.t) else '({})'
            ff = '{}' if p <= LambdaPars._get_prec(ex.f) else '({})'
            f = '{} if {} else {}'.format(ft, fc, ff)
            return f.format(LambdaPars.to_str(ex.t), LambdaPars.to_str(ex.c), LambdaPars.to_str(ex.f))
        if type(ex) is List:
            return '[{}]'.format(', '.join(map(LambdaPars.to_str, ex.vs)))
        if type(ex) is Tuple:
            if len(ex.vs) == 1:
                return '({},)'.format(LambdaPars.to_str(ex.vs[0]))
            return '({})'.format(', '.join(map(LambdaPars.to_str, ex.vs)))
        if type(ex) is Set:
            if len(ex.vs) == 0:
                return 'set()'
            return '{{{}}}'.format(', '.join(map(LambdaPars.to_str, ex.vs)))
        if type(ex) is Map:
            return '{{{}}}'.format(', '.join(map(lambda p: '{}: {}'.format(LambdaPars.to_str(p[0]), LambdaPars.to_str(p[1])), ex.vs)))
        raise TypeError(type(ex))

    def _get_prec(ex):
        if type(ex) is BinOp:
            return _bin_prec[ex.op]
        if type(ex) is UnOp:
            return _un_prec[ex.op]
        if type(ex) is Lambda:
            return 0
        if type(ex) is IfElse:
            return 2
        if type(ex) in (Attr, Call):
            return 30
        if type(ex) in (List, Tuple, Map, Set):
            return 32
        return 63

    def _find_offset(ops, offset):
        i, k = 0, len(ops)
        while i < k:
            j = (i + k) // 2
            o = ops[j].offset
            if o == offset:
                return j
            if o > offset:
                k = j
            else:
                i = j + 1
        if k == len(ops):
            return k
        raise KeyError

    def _normalize(x):
        if type(x) is IfElse:
            if type(x.t) is BinOp and x.t.op == 'or' and x.t.y == x.f:
                # c or d if b else d --> c and b or d
                return BinOp('or', BinOp('and', x.c, x.t.x), x.f)
            if type(x.t) is BinOp and x.t.op == 'and' and x.t.y == x.f and type(x.c) is UnOp and x.c.op == 'not':
                # b and c if not a else c --> (a or b) and c
                return BinOp('and', BinOp('or', x.c.x, x.t.x), x.f)
        return x

    def _parse_expr(ops, i, stack):
        for j in range(i, len(ops)):
            op = ops[j]
            opname = op.opname
            if opname == 'RETURN_VALUE':
                return stack[-1]
            if opname == 'LOAD_CONST':
                stack.append(Val(op.argval))
                continue
            if opname == 'LOAD_FAST':
                stack.append(Arg(op.argval))
                continue
            if opname in ('LOAD_GLOBAL', 'LOAD_CLOSURE', 'LOAD_DEREF'):
                stack.append(Global(op.argval))
                continue
            if opname == 'LOAD_ATTR':
                x = stack.pop()
                stack.append(Attr(op.argval, x))
                continue
            tag = _unary_lookup.get(opname, None)
            if tag:
                x = stack.pop()
                stack.append(UnOp(tag, x))
                continue
            tag = _binary_lookup.get(opname, None)
            if tag:
                y = stack.pop()
                x = stack.pop()
                stack.append(BinOp(tag, x, y))
                continue
            if opname == 'COMPARE_OP':
                y = stack.pop()
                x = stack.pop()
                stack.append(BinOp(op.argval, x, y))
                continue
            if opname == 'JUMP_IF_FALSE_OR_POP':
                jj = LambdaPars._find_offset(ops, op.argval)
                a = stack.pop()
                b = LambdaPars._parse_expr(ops[:jj], j + 1, stack[:])
                stack.append(BinOp('and', a, b))
                return LambdaPars._parse_expr(ops, jj, stack)
            if opname == 'JUMP_IF_TRUE_OR_POP':
                jj = LambdaPars._find_offset(ops, op.argval)
                a = stack.pop()
                b = LambdaPars._parse_expr(ops[:jj], j + 1, stack[:])
                stack.append(BinOp('or', a, b))
                return LambdaPars._parse_expr(ops, jj, stack)
            if opname == 'POP_JUMP_IF_FALSE':
                jj = LambdaPars._find_offset(ops, op.argval)
                k = None
                if ops[jj - 1].opname == 'JUMP_FORWARD':
                    k = LambdaPars._find_offset(ops, ops[jj - 1].argval)
                c = stack.pop()
                if k is None:
                    t = LambdaPars._parse_expr(ops, j + 1, stack[:])
                    f = LambdaPars._parse_expr(ops, jj, stack)
                    return LambdaPars._normalize(IfElse(c, t, f))
                else:
                    t = LambdaPars._parse_expr(ops[:jj - 1], j + 1, stack[:])
                    f = LambdaPars._parse_expr(ops[:k], jj, stack[:])
                    stack.append(_LambdaPars.normalize(IfElse(c, t, f)))
                    return LambdaPars._parse_expr(ops[k:], 0, stack)
            if opname == 'POP_JUMP_IF_TRUE':
                jj = LambdaPars._find_offset(ops, op.argval)
                k = None
                if ops[jj - 1].opname == 'JUMP_FORWARD':
                    k = LambdaPars._find_offset(ops, ops[jj - 1].argval)
                c = stack.pop()
                if k is None:
                    t = LambdaPars._parse_expr(ops, j + 1, stack[:])
                    f = LambdaPars._parse_expr(ops, jj, stack)
                    return LambdaPars._normalize(IfElse(UnOp('not', c), t, f))
                else:
                    t = LambdaPars._parse_expr(ops[:jj - 1], j + 1, stack[:])
                    f = LambdaPars._parse_expr(ops[:k], jj, stack[:])
                    stack.append(LambdaPars._normalize(IfElse(UnOp('not', c), t, f)))
                    return LambdaPars._parse_expr(ops[k:], 0, stack)
            if opname == 'JUMP_FORWARD':
                jj = LambdaPars._find_offset(ops, op.argval)
                return LambdaPars._parse_expr(ops, jj, stack)
            if opname == 'BUILD_LIST':
                vs = tuple(LambdaPars._popn(stack, op.argval))
                stack.append(List(vs))
                continue
            if opname == 'BUILD_TUPLE':
                vs = tuple(LambdaPars._popn(stack, op.argval))
                stack.append(Tuple(vs))
                continue
            if opname == 'BUILD_SET':
                vs = tuple(LambdaPars._popn(stack, op.argval))
                stack.append(Set(vs))
                continue
            if opname == 'BUILD_MAP':
                vs = LambdaPars._popn(stack, 2*op.argval)
                vs = tuple(zip(vs[0::2], vs[1::2]))
                stack.append(Map(vs))
                continue
            if opname == 'CALL_FUNCTION':
                args = tuple(LambdaPars._popn(stack, op.argval))
                f = stack.pop()
                stack.append(Call(f, args))
                continue
            if opname == 'MAKE_FUNCTION':
                assert op.argval in (0, 8)
                stack.pop()  
                co = stack.pop()
                if op.argval & 8:
                    stack.pop()  
                args = co.v.co_varnames
                expr = LambdaPars._parse_expr(list(dis.get_instructions(co.v)), 0, [])
                stack.append(Lambda(args, expr))
                continue
            if opname == 'NOP':
                continue
            if opname == 'POP_TOP':
                stack.pop()
                continue
            if opname == 'ROT_TWO':
                t = stack[-2]
                stack[-2] = stack[-1]
                stack[-1] = t
                continue
            if opname == 'ROT_THREE':
                t = stack[-1]
                stack[-1] = stack[-2]
                stack[-2] = stack[-3]
                stack[-3] = t
                continue
            if opname == 'DUP_TOP':
                stack.append(stack[-1])
                continue
            if opname == 'DUP_TOP_TWO':
                stack.append(stack[-2])
                stack.append(stack[-2])
                continue
            raise ValueError(op.opname)
        return stack[-1]

    def _popn(l, n):
        if not n:
            return []
        r = l[-n:]
        del l[-n:]
        return r

    def parse_lambda(f):
        assert inspect.isfunction(f)
        args = list(inspect.signature(f).parameters.keys())
        expr = LambdaPars._parse_expr(list(dis.get_instructions(f)),0,[])
        return Lambda(args, expr)
 

