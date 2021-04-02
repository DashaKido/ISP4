import os
import re

class Containter:
    def __init__(self, iterable=set()):
        self.__storage = set((str(i) for i in iterable))

    def add(self, values):
        for v in values:
            self.__storage.add(v)

    def remove(self, values):
        for v in values:
            if v in self.__storage:
                self.__storage.remove(v)

    def find(self, values):
        for v in values:
            if not v in self.__storage:
                return False
        return True

    def __str__(self):
        string = 'Container values:\n'
        for i in self.__storage:
            string += str(i)
            string += ', '
        return string.rstrip(' ,')  + '\n\n'

    def __repr__(self):
        string = str()
        for i in self.__storage:
            string += str(i)
            string += ', '
        return string.rstrip(' ,')

    def save(self, path):
        with open(path, 'w') as fp:
            fp.write(repr(self))

    def load(self, path):
        with open(path, 'r') as fp:
            string = fp.read()
        self.__storage = set((str(i) for i in string.split(', ') if i))

    def grep(self, reg_exp):
        string = str()
        for i in self.__storage:
            if re.search(reg_exp, i):
                string += i + '\n'
        return 'No matches :(' if len(string) == 0 else string

clear = lambda: os.system('cls')
valid_commands = ['a', 'r', 'f', 's', 'l', 'g', 'q']

some_list = [5, 1, -1, 0, 4, 5, 1]

container = Containter(some_list)

while True:
    clear()
    print(container)
    cmd = input('a - add\nr - remove\nf - find\nl - list\ns - save to file\nl - load from file\ng - grep\nq - quit\n\nEnter the command: ')

    if cmd not in valid_commands:
        continue

    if cmd == 'a':
        values = [x for x in input('Enter string values by space: ').split() if x]
        container.add(values)
    if cmd == 'r':
        values = [x for x in input('Enter string values by space: ').split() if x]
        container.remove(values)
    if cmd == 'f':
        values = [x for x in input('Enter string values by space: ').split() if x]
        print(container.find(values))
        input('\n\nPress Enter to continue...')
    if cmd == 's':
        path = input('Enter file name: ')
        try:
            container.save(path)
        except Exception as e:
            print('Saving failed. ERROR: ' + str(e))
            input('\n\nPress Enter to continue...')
    if cmd == 'l':
        path = input('Enter file name: ')
        try:
            container.load(path)
        except Exception as e:
            print("Loading failed. ERROR: " + str(e))
            input('\n\nPress Enter to continue...')

    if cmd == 'g':
        reg_exp = input('Enter regular expression: ')
        try:
            print(container.grep(reg_exp))
            input('\n\nPress Enter to continue...')
        except Exception as e:
            print("Grep failed. ERROR: " + str(e))
            input('\n\nPress Enter to continue...')
    if cmd == 'q':
        break
clear()
