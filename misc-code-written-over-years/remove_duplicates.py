# Sample code to remove duplicates and compress an array
# I have also included code copied from OpenAI to compress the array

import numpy as np

dups = []

ar = np.sort(np.random.randint(0,10,10)).tolist()
#print(ar)
ar =[ 0,0,1,2,2,2,3,3,3]
ar =[ 0,None,1,2,None,None,3,None,None,4]
#ar = [1,2,3,4,4]
print(ar)
ln = len(ar) 
# This is from chatGPT
def compress(arr):
    write = 0

    for read in range(len(arr)):
        if arr[read] is not None:
            arr[write] = arr[read]
            write += 1

    for i in range(write, len(arr)):
        arr[i] = None

    return arr
compress(ar)
print(ar)
#END ChatGPT
current = ar[0]
for i in range(1,len(ar)):
    if ar[i] == current:
        ar[i] = None
    else:
        current= ar[i]
print(ar)

def nextDup(none_ptr):
    global ar
    
    for i in range(none_ptr,len(ar)):
        if ar[i] is not None:
            continue
        else:
            return i
        
def nextNoneDup(ptr):
    global ar
    
    for i in range(ptr,len(ar)):
        if ar[i] is not None:
            return i
        if ptr == len(ar):
            return None
none_ptr = nextDup(0)
if none_ptr is None:
    print(ar)
    exit()

ptr=0

while True:
    # none_ptr = nextDup(none_ptr)
    # ptr = nextNoneDup(ptr)
    if ptr > none_ptr:
        ar[none_ptr] = ar[ptr]
        ar[ptr] = None
        none_ptr = nextDup(none_ptr+1)
        ptr = nextNoneDup(ptr+1)
    else:
        ptr = nextNoneDup(ptr+1)
    if ptr is None:
        break

    print(ptr)
    print(none_ptr)
    if ptr >=ln or none_ptr >=ln:
        break

print(ar)
