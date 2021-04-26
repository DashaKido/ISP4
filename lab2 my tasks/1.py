#статистика по тексту
text = 'aa aa aa sa sa sa dd ww '

lst_no = ['.', ',', ':', '!', '"', "'", '[', ']', '-', '—', '(', ')', '?', '_', '`'  ]   # и т.д.
lst = []

for word in text.lower().split():
    if not word in lst_no:
        _word = word 
        if word[-1] in lst_no:
            _word = _word[:-1]
        if word[0] in lst_no:
            _word = _word[1:] 
        lst.append(_word)

_dict = dict()
for word in lst:
    _dict[word] = _dict.get(word, 0) + 1

# сортируем словарь посредством формирования списка (значение, ключ)
_list = []
count = 0
for key, value in _dict.items():
    _list.append((value, key))
    _list.sort(reverse=False)
    count += value

print('все слова + сколько повторяются: ',_list)
res = count/len(_list)
print('среднее кол-во слов:',res)

