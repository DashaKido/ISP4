from .constants import *
from .converter import *
#СИНТАКСИЧЕСКИЙ АНАЛИЗ
#получают список лексем и пытаются найти закономерности,
#соответствующие языку

#обрабатывает рекурсивные структуры(деревья и тд)

#парсинг массивов
#ищет [ 
#далее поиск элементов массива, запятых между ними или же ]
def parse_array(tokens, flag=''):
    array = []
    t = tokens[0]
    #если первый элемент ]
    if t == JSON_RIGHTBRACKET:
        #работа с флагами и возврат сответствующих типов данных
        if flag == JSON_TUPLE_FLAG:
            return tuple(array), tokens[1:]
        if flag == JSON_SET_FLAG:
            return set(array), tokens[1:]
        return array, tokens[1:]
    #проходим по массиву пока не найдем ]
    while t != JSON_RIGHTBRACKET:
        #вызывем парсер
        result, tokens = parse(tokens)
        #добавляем данные к списку
        array.append(result)
        #делаем тоже самое что выше описано
        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            if flag == JSON_TUPLE_FLAG:
                return tuple(array), tokens[1:]            
            if flag == JSON_SET_FLAG:
                return set(array), tokens[1:]            
            return array, tokens[1:]
        #если не нашли , то исключение
        elif t != JSON_COMMA:
            raise SyntaxError('Expected comma after object in array')
        #если все нормально то считываем со 2 элемента
        else:
            tokens = tokens[1:]

    raise SyntaxError('Expected end-of-array bracket')

#парсинг обьектов
#поиск пар ключ-значение, где ключ от значения отделен :
#пары разделены ,
#поиск идет до конца обьекта
def parse_object(tokens, flag=''):
    obj = {}

    t = tokens[0]
    #если первый элемент }
    if t == JSON_RIGHTBRACE:
        #возвращаем обьект и массив начиная со 2 элемента
        return obj, tokens[1:]
    #пока элемент не равен }
    while t != JSON_RIGHTBRACE:
        #если нашли какой-то из флагов то парсим как массив
        if len(tokens) > 1 and tokens[0] == JSON_TUPLE_FLAG and tokens[1] == '[':
            key, tokens = parse_array(tokens[2:], JSON_TUPLE_FLAG)
        else:
        #если нет то 
        #1 элемент ключ, а далее считвычаем дальше
            key = tokens[0]
            tokens = tokens[1:]
        #если 1 элемент не : - исключение
        if tokens[0] != JSON_COLON:
            raise SyntaxError('Expected colon after key in object, got: {}'.format(t))
        #парсим наши внутренние значения
        value, tokens = parse(tokens[1:])

        obj[key] = value

        t = tokens[0]
        #если 1 элемент ]
        if t == JSON_RIGHTBRACE:
            #и флаг словаря 
            if flag == JSON_DICT_FLAG:
                #возвращаем обьект и массив со 2 элемента
                return obj, tokens[1:]
            #если нет то идем в конвертер 
            else:
                return dict_to_obj(obj), tokens[1:]
        #если элемент не : - исключение
        elif t != JSON_COMMA:
            raise SyntaxError('Expected comma after pair in object, got: {}'.format(t))
        #сиитываем со 2 элемента
        tokens = tokens[1:]

    raise SyntaxError('Expected end-of-object bracket')
#определяем что именно парсить 
def parse(tokens, flag=''):
    #работа с флагами
    if tokens[0] in JSON_FLAGS:
        flag = tokens[0]
        tokens = tokens[1:]

    t = tokens[0]
    #если [ парсим как массив
    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:], flag)
    #если { парсим как обьект
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:], flag)
    #просто возвращаем 1 элемент и массив начиная со 2
    else:
        return t, tokens[1:]
