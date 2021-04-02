import re

s = "Natural-language processing (NLP) is an area of computer science " \
    "and artificial intelligence concerned with the interactions " \
    "between computers and human (natural) languages."

s = s.split(' ')

d = {}

for word in s:
    m = re.match(r'[a-zA-Z]+', word)

    if m is not None:
        if m.group(0) in d.keys():
            d[m.group(0)] += 1
        else:
            d[m.group(0)] = 1

d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

for k, v in list(d.items())[:5]:
    print(f'{k}: {v}')