def binary(arr,find, first=0,last=None):
    if first<0:
        raise Exception("negative!!")
    if last is None:
        last = len(arr)
    while first < last:
        mid = int((first+last)/2)
        if arr[mid]<find:
            first = mid+1
        else:
            last = mid
    return first
        

if __name__ == "__main__":
    d=[1,2,3,4,5]
    print(binary(d,4))