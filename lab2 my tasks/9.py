#свой range
def _range(start: int, stop=None, step=1, skip=0) -> iter:
    if stop is None:
        stop = start
        start = 0

    i = 1
    while start < stop:
        if i == skip:
            i = 1
        else:
            yield start
            i += 1
        start += step

print(list(range(1, 12, 1)))
print(list(_range(1, 12, 1)))
print(list(_range(1, 12, skip=2)))
