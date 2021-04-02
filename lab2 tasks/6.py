class DictItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __getitem__(self, key):
        if key == self.key:
            return self.value
    
    def __setitem__(self, key, value):
        if key == self.key:
            self.value = value
        else:
            if type(self.value) != Dict:
                self.value = Dict()

            self.value._Dict__append_item(DictItem(key, value))

    def __str__(self):
        return str(self.value)

class Dict:
    def __init__(self):
        self.__d = list()

    def __find_node(self, d, key):
        for item in d:
            if item.key == key:
                return item
            if type(item.value) == Dict:
                res = Dict.__getitem__(item.value, key)
                if res != None:
                    return res

    def __append_item(self, item):
        self.__d.append(item)

    def __is_hashable(v):
        try:
            hash(v)
        except TypeError:
            return False
        return True        

    def __getitem__(self, key):
        item = self.__find_node(self.__d, key)
        if not item is None and type(item.value) == Dict:
            return item.value
        return item
    
    def __setitem__(self, key, value):
        if not Dict.__is_hashable(key):
            raise KeyError('Unhashable key')

        item = self.__find_node(self.__d, key)
        if item == None:
            self.__d.append(DictItem(key, value))
        else:
            item.value = value

    def __str__(self):
        string = '{ '
        for item in self.__d:
            if type(item.value) == Dict:
                string += f'"{item.key}": ' + Dict.__str__(item.value) + ', '
            else:
                if type(item.key) == str:
                    string += f'"{item.key}": {item.value}, '
                else:
                    string += f'{item.key}: {item.value}, '
        return string.rstrip(', ') + ' }'


d = Dict()

d['a'] = 1
print(d)

d['a']['b'] = 2
print(d)

d['a']['b']['c'] = 3
print(d)

d[(1, 2)] = 1
print(d)

d['a']['b']['e'] = True
print(d)

d['a'][2] = [None, True]
print(d)

print('\n')
print(d['a']['b'])

print(d[(1, 2)])

print(d['a'][2])
print()
