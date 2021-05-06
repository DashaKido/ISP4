from .constants import *
import inspect
#ЛЕКСИЧЕСКИЙ АНАЛИЗ
#разбиваются исходные данные на элементы языка(токены)
#пробелы и комментарии пропускаются
#всегда возвращает одномерный список токенов

#определение строк
def lex_string(string):
    result = ''
    #сразу проверка является ли 1 символ кавычкой
    if string[0] == JSON_QUOTE:
    #если да, то поиск идет дальше пропуская 1 символ в строке
        string = string[1:]
    else:
    #null если ничего не нашли + исходный список
        return None, string
    #перебираем значения внутри кавычев
    for c in string:
        #если нашли ",то вернется строка внутри кавычек + остальна часть непровер строки  
        if c == JSON_QUOTE:            
            return result, string[len(result)+1:]
        #если нет, то берем след элемент
        else:
            result += c
    #если что-то пошло не так то исключение   
    raise SyntaxError('Expected end of string quote')
#определение чисел
def lex_number(string):
    result = ''
    #переменная содержащая части числа
    number_characters = [str(digit) for digit in range(0, 10)] + ['-', 'e', '.']
    #итерируемся по входящей строке
    for c in string:
        #пока не найдем знак, который не может быть частью числа
        if c in number_characters:
            result += c
        else:
            break
    #перемнная содержащая нашу строку
    rest = string[len(result):]
    #возвращаем или float или int
    try:
        if '.' in result:
            return float(result), rest
        return int(result), rest
    except:
    #или null + исходная строка если ничего не нашли 
        return None, string
#определение булевых значений
def lex_bool(string):
    string_len = len(string)
    #простое совпадение строк
    if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string
#определение null
def lex_null(string):
    string_len = len(string)
     #простое совпадение строк
    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]

    return None, string
#выделяем из ввода числа, строки, бул. зач и null
def lex(string):
    tokens = []
    #проходим по всей строки
    while len(string):
        #вызываем определение строк
        result, string = lex_string(string)
        #если строка не пустая 
        if result is not None:
            try:
                d = {}
                #вызывается метод, который возвращает копию строки
                # в которой все символы с начала и конца были удалены
                fixed_result = result.strip()
                #если наша строка содержит self
                if fixed_result.startswith('self.'):
                    fixed_result = fixed_result[5:]
                #если наша строка содержит @
                if fixed_result.startswith('@'):
                    #пока не найдем начало функции
                    while len(fixed_result) > 3 and fixed_result[:3] != 'def':
                        fixed_result = fixed_result[3:]
                #если таких подстрок нет то ошибка
                if fixed_result.find('class') == -1 and fixed_result.find('def') == -1 and fixed_result.find('lambda') == -1:
                    raise Exception('Not valid class or function')

                #динамически исполняет код
                #по факту извлекает код из 1 аргумента и записывает в словарь
                #тк мы передаем пустой словарь, то обьекту доступны только __builtins__
                exec(fixed_result, d)
                #проходим по нашему словарю
                for k in d:
                    #доступ к встроенным функциям питона
                    if k != '__builtins__':
                        #если обьект можно вызвать или обьект является классом
                        if callable(d[k]) or inspect.isclass(d[k]):
                            #добавление элементов к списку
                            tokens.append(d[k])
                            break
                        #если что-то пошло не так - исключение
                        raise Exception('Not valid class or function')
                continue
            except Exception as e:
                #добавление элементов к списку
                tokens.append(result)
                continue
        #вызываем определение чисел
        result, string = lex_number(string)
        #если строка не пустая
        if result is not None:
            #добавляем элементы к списку
            tokens.append(result)
            continue
        #вызываем определение булевых переменных
        result, string = lex_bool(string)
        if result is not None:
            tokens.append(result)
            continue
        #вызываем определение null
        result, string = lex_null(string)
        if result is not None:
            tokens.append(None)
            continue
        #если первый элемент в строке пробел
        if string[0] in JSON_WHITESPACE:
            #считываем начиная со 2
            string = string[1:]
        #если 1 символ является частью языка JSON ли является флагом
        elif string[0] in JSON_SYNTAX or string[0] in JSON_FLAGS:
            #добавляем элемент к списку
            tokens.append(string[0])
            #и считываем начиная со 2
            string = string[1:]
        #если что-то пошло не так - исключение
        else:
            raise SyntaxError('Unexpected character: {}'.format(string[0]))
    #возвращаем одномерный массив лексем
    return tokens
