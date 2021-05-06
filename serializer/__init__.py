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
    
    #РАБОТА С ЛЯМБДА
    #приобразуем выражение в строку
    def to_str(ex):
        #если лямбда
        if type(ex) is Lambda:
            #если обьект содержит аргументы
            if ex.args:
                #возвращаем строку собранную из аргументов обьекта,поддерживающего итерирование
                #и вызываем метод to_str для выражения после :
                return 'lambda {}: {}'.format(', '.join(ex.args),JsonSer.to_str(ex.expr))
            #вызываем метод для выражения после :
            return 'lambda: {}'.format(JsonSer.to_str(ex.expr))
        if type(ex) is Val:
            #возвращаем значения ввиде строки
            return str(ex.v)
        if type(ex) in (Arg, Global):
            #возвращаем число ввиде строки
            return str(ex.n)
        if type(ex) is Attr:
            #вызываем метол соответствия
            p = JsonSer._get_prec(ex)
            if p > JsonSer._get_prec(ex.x):
                #вызываем метод to_str для выражения
                return '({}).{}'.format(JsonSer.to_str(ex.x), ex.n)
            #вызываем метод to_str для выражения
            return '{}.{}'.format(JsonSer.to_str(ex.x), ex.n)
        if type(ex) is BinOp:
            #вызываем метол соответствия
            p = JsonSer._get_prec(ex)
            if ex.op == '[]':
                if p > JsonSer._get_prec(ex.x):
                    #вызываем метод to_str для выражения
                    return '({})[{}]'.format(JsonSer.to_str(ex.x), JsonSer.to_str(ex.y))
                return '{}[{}]'.format(JsonSer.to_str(ex.x), JsonSer.to_str(ex.y))
            #вызываем метол соответствия
            fx = '{}' if p <= JsonSer._get_prec(ex.x)&62 else '({})'
            fy = '{}' if p|1 <= JsonSer._get_prec(ex.y) else '({})'
            f = fx + ' {} ' + fy
            #вызываем метод to_str для выражения
            return f.format(JsonSer.to_str(ex.x), ex.op, JsonSer.to_str(ex.y))
        if type(ex) is UnOp:
            t = ex.op
            #возвращает флаг указывающий на то является ли символ буквой
            if t[-1].isalpha():
                t = t + ' '
                #сравнение вызовов методов соответствия
            if JsonSer._get_prec(ex) > JsonSer._get_prec(ex.x):
                return '{}({})'.format(t, JsonSer.to_str(ex.x))
            #и вызываем метод to_str для выражения
            return '{}{}'.format(t, JsonSer.to_str(ex.x))
        if type(ex) is Call:
             #сравнение вызовов методов соответствия
            if JsonSer._get_prec(ex) > JsonSer._get_prec(ex.f):
                #возвращаем строку собранную из аргументов обьекта,поддерживающего итерирование
                #мар применение указанной функции к каждому элементу последовательности
                #и вызываем метод to_str для выражения после :
                return '({})({})'.format(JsonSer.to_str(ex.f), ', '.join(map(JsonSer.to_str, ex.args)))
            return '{}({})'.format(JsonSer.to_str(ex.f), ', '.join(map(JsonSer.to_str, ex.args)))
        if type(ex) is IfElse:
            #вызов метода соответствия
            p = JsonSer._get_prec(ex)
            fc = '{}' if p < JsonSer._get_prec(ex.c) else '({})'
            ft = '{}' if p < JsonSer._get_prec(ex.t) else '({})'
            ff = '{}' if p <= JsonSer._get_prec(ex.f) else '({})'
            f = '{} if {} else {}'.format(ft, fc, ff)
            #и вызываем метод to_str для выражения
            return f.format(JsonSer.to_str(ex.t), JsonSer.to_str(ex.c), JsonSer.to_str(ex.f))
        if type(ex) is List:
            #возвращаем строку собранную из аргументов обьекта,поддерживающего итерирование
                #мар применение указанной функции к каждому элементу последовательности
                #и вызываем метод to_str для выражения после :
            return '[{}]'.format(', '.join(map(JsonSer.to_str, ex.vs)))
        if type(ex) is Tuple:
            if len(ex.vs) == 1:
                return '({},)'.format(JsonSer.to_str(ex.vs[0]))
            return '({})'.format(', '.join(map(JsonSer.to_str, ex.vs)))
        if type(ex) is Set:
            if len(ex.vs) == 0:
                return 'set()'
            return '{{{}}}'.format(', '.join(map(JsonSer.to_str, ex.vs)))
        if type(ex) is Map:
            return '{{{}}}'.format(', '.join(map(lambda p: '{}: {}'.format(JsonSer.to_str(p[0]), JsonSer.to_str(p[1])), ex.vs)))
        raise TypeError(type(ex))
    #метода соответствия
    def _get_prec(ex):
        #проверка на соответствие типу и возврат значения
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
    #метод смещения
    def _find_offset(ops, offset):
        i, k = 0, len(ops)
        while i < k:
            j = (i + k) // 2
            #начальный индекс операции в последовательности байт-кодов
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
    #метод нормализования
    def _normalize(x):
        #если соответствует типу
        if type(x) is IfElse:
            if type(x.t) is BinOp and x.t.op == 'or' and x.t.y == x.f:
                # c or d if b else d --> c and b or d
                return BinOp('or', BinOp('and', x.c, x.t.x), x.f)
            if type(x.t) is BinOp and x.t.op == 'and' and x.t.y == x.f and type(x.c) is UnOp and x.c.op == 'not':
                # b and c if not a else c --> (a or b) and c
                return BinOp('and', BinOp('or', x.c.x, x.t.x), x.f)
        return x
#парсинг выражений
    def _parse_expr(ops, i, stack):
        #проходим по всему обьекту 
        for j in range(i, len(ops)):
            op = ops[j]
            #читаемое для человека имя для операции
            opname = op.opname
            #TOS(top-os-stack) верхушка стека
            #возвращает TOS вызывающей функции
            if opname == 'RETURN_VALUE':
                #возвращает последнее значение
                return stack[-1]
            #вталкивает co_consts[consti] в стек
            if opname == 'LOAD_CONST':
                #добавляет значение в стэк
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(Val(op.argval))
                continue
            #вталкивает ссылку на локальную co_varnames[var_num]в стек
            if opname == 'LOAD_FAST':
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(Arg(op.argval))
                continue
            #загружает глобальные имена в стек
                #вталкивает ссылку в ячейку, содержащуюся в слоте i ячейки и свободное 
                #хранилище переменных
            #загружает ячейку, содержащуюся в слоте i ясейки, и свободное хранилище переменых
            if opname in ('LOAD_GLOBAL', 'LOAD_CLOSURE', 'LOAD_DEREF'):
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(Global(op.argval))
                continue
            #заменяет TOS на getattr(TOS,co_names[namei])                
            if opname == 'LOAD_ATTR':
                #возврат элемента, удаляя его из списка
                x = stack.pop()
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(Attr(op.argval, x))
                continue
            #возвращает значение из словаря по ключу
            tag = _unary_lookup.get(opname, None)
            if tag:
                #возврат элемента, удаляя его из списка
                x = stack.pop()
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(UnOp(tag, x))
                continue
            tag = _binary_lookup.get(opname, None)
            if tag:
                #возврат элемента, удаляя его из списка
                y = stack.pop()
                x = stack.pop()
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(BinOp(tag, x, y))
                continue
            #выполняет логическую операцию
            if opname == 'COMPARE_OP':
                y = stack.pop()
                x = stack.pop()
                stack.append(BinOp(op.argval, x, y))
                continue
            #если TOS содержит false, устанавливает счетчик байт-кодов в значение target
            #и оставляет TOS в стеке
            #в противном случае выталкивает TOS
            if opname == 'JUMP_IF_FALSE_OR_POP':
                #вызываем метод смещения
                jj = JsonSer._find_offset(ops, op.argval)
                #возврат элемента, удаляя его из списка
                a = stack.pop()
                #вызываем еще раз парсинг выражений для оставшейся части
                b = JsonSer._parse_expr(ops[:jj], j + 1, stack[:])
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(BinOp('and', a, b))
                #вызваем еще раз для всего? выражения
                return JsonSer._parse_expr(ops, jj, stack)
            #если TOS содержит true, устанавливает счетчик байт-кодов в значение target
            #и оставляет TOS в стеке
            #в противном случае выталкивает TOS
            if opname == 'JUMP_IF_TRUE_OR_POP':
                #вызываем метод смещения
                jj = JsonSer._find_offset(ops, op.argval)
                #возврат элемента, удаляя его из списка
                a = stack.pop()
                #вызываем еще раз парсинг выражений для оставшейся части 
                b = JsonSer._parse_expr(ops[:jj], j + 1, stack[:])
                #добавлет в стек значение
                #значение =разрешенное op значение(если известно), иначе такое же как op
                stack.append(BinOp('or', a, b))
                #вызваем еще раз для всего? выражения
                return JsonSer._parse_expr(ops, jj, stack)
            #если TOS содержит false,задает для счетчика
            # байт-кодов значение target
            #всплывет TOS
            if opname == 'POP_JUMP_IF_FALSE':
                #вызываем метод смещения
                jj = JsonSer._find_offset(ops, op.argval)
                k = None
                #читаемое человеком имя
                #увеличивает счетчик байт-кодов на delta
                if ops[jj - 1].opname == 'JUMP_FORWARD':
                    #вызываем метод смещения
                    k = JsonSer._find_offset(ops, ops[jj - 1].argval)
                #возврат элемента, удаляя его из списка
                c = stack.pop()
                if k is None:
                    #вызываем еще раз парсинг выражений
                    t = JsonSer._parse_expr(ops, j + 1, stack[:])
                    f = JsonSer._parse_expr(ops, jj, stack)
                    #возвращаем вызов метода нормализования
                    return JsonSer._normalize(IfElse(c, t, f))
                else:
                    #вызываем еще раз парсинг выражений
                    t = JsonSer._parse_expr(ops[:jj - 1], j + 1, stack[:])
                    f = JsonSer._parse_expr(ops[:k], jj, stack[:])
                    #добавляем в стек результат вызова метода нормализования
                    stack.append(_JsonSer.normalize(IfElse(c, t, f)))
                    #вызываем еще раз парсинг выражений
                    return JsonSer._parse_expr(ops[k:], 0, stack)
            #если TOS содержит trut,задает для счетчика
            # байт-кодов значение target
            #выталкиевает TOS
            if opname == 'POP_JUMP_IF_TRUE':
                #вызываем метод смещения
                jj = JsonSer._find_offset(ops, op.argval)
                k = None
                #читаемое человеком имя
                #увеличивает счетчик байт-кодов на delta
                if ops[jj - 1].opname == 'JUMP_FORWARD':
                    #вызываем метод смещения
                    k = JsonSer._find_offset(ops, ops[jj - 1].argval)
                #возврат элемента, удаляя его из списка
                c = stack.pop()
                if k is None:
                    #вызываем еще раз парсинг выражений
                    t = JsonSer._parse_expr(ops, j + 1, stack[:])
                    f = JsonSer._parse_expr(ops, jj, stack)
                    #возвращаем вызов метода нормализования
                    return JsonSer._normalize(IfElse(UnOp('not', c), t, f))
                else:
                    #вызываем еще раз парсинг выражений
                    t = JsonSer._parse_expr(ops[:jj - 1], j + 1, stack[:])
                    f = JsonSer._parse_expr(ops[:k], jj, stack[:])
                    #добавляем в стек результат вызова метода нормализования
                    stack.append(JsonSer._normalize(IfElse(UnOp('not', c), t, f)))
                    #вызываем еще раз парсинг выражений
                    return JsonSer._parse_expr(ops[k:], 0, stack)
            #увеличивает счетчик байт-кодов на delta
            if opname == 'JUMP_FORWARD':
                #вызываем метод смещения
                jj = JsonSer._find_offset(ops, op.argval)
                #вызываем еще раз парсинг выражений
                return JsonSer._parse_expr(ops, jj, stack)
            #создает список, потребляющие count элементов из стека,
            #и вталкавает полученный список в стек
            if opname == 'BUILD_LIST':
                #создает кортеж из вызова метода _popn
                vs = tuple(JsonSer._popn(stack, op.argval))
                #обавляет элементы в стек
                stack.append(List(vs))
                continue
            #создает кортеж, потребляющие count элементов из стека,
            #и вталкавает полученный кортеж в стек
            if opname == 'BUILD_TUPLE':
                #создает кортеж из вызова метода _popn
                vs = tuple(JsonSer._popn(stack, op.argval))
                #обавляет элементы в стек
                stack.append(Tuple(vs))
                continue
            #создает множество, потребляющие count элементов из стека,
            #и вталкавает полученное множество в стек
            if opname == 'BUILD_SET':
                #создает кортеж из вызова метода _popn
                vs = tuple(JsonSer._popn(stack, op.argval))
                #обавляет элементы в стек
                stack.append(Set(vs))
                continue
            #перемещает новый обькт словаря в стек 
            if opname == 'BUILD_MAP':
                #вызывается метод _popn
                vs = JsonSer._popn(stack, 2*op.argval)
                #кортеж из возвращаемого итератора по кортежам
                vs = tuple(zip(vs[0::2], vs[1::2]))
                 #обавляет элементы в стек
                stack.append(Map(vs))
                continue
            #вызывает вызываемый обьект с позиционными аргументами
            if opname == 'CALL_FUNCTION':
                #создает кортеж из вызова метода _popn
                args = tuple(JsonSer._popn(stack, op.argval))
                #возвращаем элемент, удаляя его из списка
                f = stack.pop()
                #обавляет элементы в стек
                stack.append(Call(f, args))
                continue
            #вталкивает новый обьект функции в стек
            if opname == 'MAKE_FUNCTION':
                #для проверки истинности
                assert op.argval in (0, 8)
                #возвращаем элемент, удаляя его из списка
                stack.pop()  
                #возвращаем элемент, удаляя его из списка
                co = stack.pop()
                if op.argval & 8:
                    #возвращаем элемент, удаляя его из списка
                    stack.pop()  
                args = co.v.co_varnames
                #вызываем еще раз парсинг выражений
                expr = JsonSer._parse_expr(list(dis.get_instructions(co.v)), 0, [])
                #обавляет элементы в стек
                stack.append(Lambda(args, expr))
                continue
            #ничего не делающий код
            #используется в качестве местозаполнения оптимизатором байт-кодов
            if opname == 'NOP':
                continue
            #удаляет верхний элемент из стека
            if opname == 'POP_TOP':
                #возвращаем элемент, удаляя его из списка
                stack.pop()
                continue
            #замена 2 самых верхних элементов стека
            if opname == 'ROT_TWO':
                t = stack[-2]
                stack[-2] = stack[-1]
                stack[-1] = t
                continue
            #поднимает второй и третий элемент стека на одну позицию вверх
            #перемещает сверху вниз в позицию три
            if opname == 'ROT_THREE':
                t = stack[-1]
                stack[-1] = stack[-2]
                stack[-2] = stack[-3]
                stack[-3] = t
                continue
            #дублирует ссылку верхней части стека
            if opname == 'DUP_TOP':
                #добавляет значение в стэк
                stack.append(stack[-1])
                continue
            #дублирует 2 ссылки вершины стека, оставляя их в том же порядке
            if opname == 'DUP_TOP_TWO':
                #добавляет значение в стэк
                stack.append(stack[-2])
                stack.append(stack[-2])
                continue
            #если что-то пошло не так ошибка имени
            raise ValueError(op.opname)
        #возвращает последнее значение
        return stack[-1]

    def _popn(l, n):
        if not n:
            return []
        r = l[-n:]
        del l[-n:]
        return r
#синтаксический анализ лямбды
    def parse_lambda(f):
        #если истинности выражения
        #если передаваемый обьект являемся функцией
        assert inspect.isfunction(f)
        #аргументы это списка из возвращаемых ключей сигнатуры
        args = list(inspect.signature(f).parameters.keys())
        #для выражения вызываем метод парсинга с агрументами в виде списка
        #итераторов над инструкциями 
        #итератор генерирует ряд инструкций в виде именновованных кортежей, 
        #дающих ведения о каждой операции в коде
        expr = JsonSer._parse_expr(list(dis.get_instructions(f)),0,[])
        #возвращаем именнованный кортеж с аргументами и выражениями
        return Lambda(args, expr)
 

