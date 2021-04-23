import inspect
import types
#класс для обновления словаря
class ObjectBuilder:
    def __init__(self, **entries):
        #обновляем атрибут __dict__(который представляет атрибуты класса в форме словаря)
        #при совпадении ключей значения заменяются
        self.__dict__.update(entries)
#методы привязки
def bind_methods(instance):
    #переменная содержащая словарь из
    #возвращаемых атрибутов обьекта instance которые имею тип функции 
    methods = dict(inspect.getmembers(instance, inspect.isfunction))
    #проходим по словарю
    for method in methods:
        cur_method = methods[method]
        #переменная содержащая словарь из
        #возвращает параметры сигнатуры
        args = list(inspect.signature(cur_method).parameters)
        #если есть self 
        if len(args) > 0 and args[0] == 'self':
            #для каждого обькта вызываем метод привязка
            bind_method(instance, cur_method)
#метод привязки
def bind_method(instance, func, as_name=None):
    #если имя пустое
    if as_name == None:
        #присваиваем переменной название передаваемой функции
        as_name = func.__name__
    #определяем значение, возвращаемое дескриптором
    #instance экземпляр класса владельца дескриптора
    #2 аргумент класс владельца дескриптора(ссылка на класс instance)
    bound_method = func.__get__(instance, instance.__class__)
    #добавляем обьекту атрибут с названием и значением
    setattr(instance, as_name, bound_method)
#функция переводящая словать в обьект
def dict_to_obj(d):
    #если наш объект не словарь
    if type(d) != dict:
        #возвращаем обьект
        return d
    #создаем обьект класса
    top = ObjectBuilder(**d)
    #возвращая пары(ключ,значение) для каждого элемента словаря
    for i, j in d.items():
        #добавляем обьекту top наши пары
        setattr(top, i, j)
    #методы привязки
    bind_methods(top)
    #возвращаем наш экземпляр класса
    return top
#функция переводящая обьект в словать
def obj_to_dict(obj):
    #проверяем содержит ли обьект атрибут __iter__
    #и обьект не строка
    if hasattr(obj, "__iter__") and type(obj) != str:
        #возвращаем обьект
        return type(obj)([v for v in obj])
    #проверяем содержит ли обьект атрибут __dict__
    #го нельзя вызвать
    elif hasattr(obj, "__dict__") and not callable(obj):
        #устанавливаем аттрибуты
        attributes = [(key, value) 
                    #возвращаем все атрибуты обьекта
                    for key, value in inspect.getmembers(obj)
                    #если они не начинаются с _ и их нельзя вызвать
                    if not key.startswith('_') and not callable(value) 
                    #и значение не является методом
                    and not inspect.ismethod(value)]
        #устанавливаем методы
        #возвращаем все атрибуты обьекта которые относятся к лямбда
        methods = inspect.getmembers(obj, lambda a: inspect.ismethod(a) 
                                    or type(a) == types.LambdaType)
        #словарь с атрибутами и методами
        d = dict(attributes + methods)
        #проверяем содержит ли обьект атрибут __class__
        if hasattr(obj, '__class__'):
            #присваеваем словарю с ключем __class__ значение исходного программного кода обьекта в виде единственной строки
            #данное значение это возвращаемное значение атрибута обькта заменяем при этом кавычки
            d['__class__'] = inspect.getsource(getattr(obj, '__class__')).replace('"', "'")
        #возвращаем наш словарь
        return d
    else:
        #или возвращаем наш исходный обьект
        return obj
#функция для проверки типов      
def is_primitive(obj):
    #возвращаем тип обьекта
    return type(obj) in [int, float, str, bool, type(None)]
#проверка на обьект или словарь
def is_object_or_dict(obj):
    #возвращаем если не явлется приметивным типом, нельзя вызвать или это не класс
    return not (type(obj) in [int, float, str, bool, type(None), list, tuple, set]
                or callable(obj) or inspect.isclass(obj))
