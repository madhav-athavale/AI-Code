import numpy as np
ary = []
ary = np.random.randint(0,10,10)
ary.sort()

def rotateRight(ary, num):
    newAry = []
    
    for i in range(num):
        newAry.append(ary[len(ary)-i-1])
    print(newAry)
    print(ary)
    # print(len(ary))
    # for i in range(len(ary)-1):
    #     print(i)
    #     print(ary[len(ary)-1 -num -i])

    for i in range(len(ary)-1):
       
       
        ary[len(ary)-1-i] = ary[len(ary)-1 -num -i]
  

    for i in range(len(newAry)):
        print(i)
        ary[num-1-i] = newAry[i]

    print(ary)

def findMin(ary):
    ln = len(ary)-1
    for i in range(len(ary)-1):
        if ary[ln-i-1] > ary[ln-i]:
            print(ary[ln-i])
        


rotateRight(ary, 8)
findMin(ary)