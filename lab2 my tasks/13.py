def qs(s_arr, first, last):
    if (first < last):
        left = first
        right = last
        ind = int((left + right) / 2)
        
        middle = s_arr[ind]
        while (s_arr[left] < middle):
            left=left+1

        while (s_arr[right] > middle):
            right=right-1

        if (left <= right):
            tmp = s_arr[left]
            s_arr[left] = s_arr[right]
            s_arr[right] = tmp
            left=left+1
            right=right-1

        while(left < right):
            while (s_arr[left] < middle):
                left=left+1

            while (s_arr[right] > middle):
                right=right-1

            if (left <= right):
                tmp = s_arr[left]
                s_arr[left] = s_arr[right]
                s_arr[right] = tmp
                left=left+1
                right=right-1

        qs(s_arr, first, right)
        qs(s_arr, left, last)

def merge_two_lists(a, b):
    c=[]
    i=j=0
    while i<len(a) and j<len(b):
        if a[i]<b[j]:
            c.append(a[i])
            i+=1
        else:
            c.append(b[j])
            j+=1
    if i<len(a):
        c+=a[i:]
    if j<len(b):
        c+=b[j:]
    return c

def merge_sort(s):
    if len(s)==1:
        return s
    middle = int(len(s)/2)
    left = merge_sort(s[:middle])
    right = merge_sort(s[middle:])
    return merge_two_lists(left,right)

def countingSort(arr,exp1):
    n = len(arr)
    output = [0]*(n)
    count = [0]*(10)
    for i in range(0,n):
        index = (arr[i]/exp1)
        count[int(index%10)]+=1
    for i in range(1,10):
        count[i]+=count[i-1]
    i=n-1
    while i>=0:
        index = (arr[i]/exp1)
        output[count[int(index%10)]-1]=arr[i]
        count[int(index%10)]-=1
        i-=1
    i=0
    for i in range(0,len(arr)):
        arr[i] = output[i]
        
def radix_sort(arr):
    max1=max(arr)
    exp=1
    while max1/exp>0:
        countingSort(arr,exp)
        exp*=10
    
if __name__ == "__main__":
    arr = [1,3,5,2,4]
    print(arr)
    qs(arr,0,4)
    print(arr)
    arr = [1,3,5,2,4]
    print()
    print(arr)
    print(merge_sort(arr))
    arr = [1,3,5,2,4]
    print()
    print(arr)
    radix_sort(arr)
    print(arr)

