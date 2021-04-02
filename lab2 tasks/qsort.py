import random

def qsort(a, l=None, r=None):
    if l == None or r == None:
        l = 0
        r = len(a) - 1

    x = a[(l + r) // 2]

    i = l
    j = r

    while i <= j:
        while a[i] < x:
            i += 1
        while a[j] > x:
            j -= 1
        
        if i <= j:
            t = a[i]
            a[i] = a[j]
            a[j] = t
            i += 1
            j -= 1

    if l < j:
        qsort(a, l, j)
    if r > i:
        qsort(a, i, r)

a = [random.randint(1,10) for _ in range(100)]

qsort(a)

print(a)