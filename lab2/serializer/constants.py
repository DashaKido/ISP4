from collections import namedtuple

JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'
JSON_QUOTE = '"'

JSON_DICT_FLAG = 'D'
JSON_TUPLE_FLAG = 'T'
JSON_SET_FLAG = 'S'

JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

JSON_FLAGS = [JSON_DICT_FLAG, JSON_TUPLE_FLAG, JSON_SET_FLAG]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')
#именованные кортежи 
#не могут быть изменены после создания
Lambda = namedtuple('Lambda', ['args', 'expr'])
Val = namedtuple('Val', ['v'])
Arg = namedtuple('Arg', ['n'])
Global = namedtuple('Global', ['n'])
BinOp = namedtuple('BinOp', ['op', 'x', 'y'])
UnOp = namedtuple('UnOp', ['op', 'x'])
IfElse = namedtuple('IfElse', ['c', 't', 'f'])
Attr = namedtuple('Attr', ['n', 'x'])
List = namedtuple('List', ['vs'])
Tuple = namedtuple('Tuple', ['vs'])
Map = namedtuple('Map', ['vs'])
Set = namedtuple('Set', ['vs'])
Call = namedtuple('Call', ['f', 'args'])
#тут они не работают
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