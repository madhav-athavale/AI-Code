import numpy as np

ar1 = [1,3,5,8,12,14]
ar2 = [2,6,9,11]
ar3 = []
ln1 = len(ar1)
ln2 = len(ar2)
i =0
j =0
while i < ln1 and j < ln2:
    if ar1[i] < ar2[j]:
        ar3.append(ar1[i])
        i = i+ 1
    elif ar1[i] > ar2[j]:
        ar3.append(ar2[j])
        j = j + 1
    else:
        ar3.append(ar1[i])
        ar3.append(ar2[j])
        i = i +1
        j = j+ 1


for k in range(i,ln1) :
    ar3.append(ar1[k])
    
for k in range(j,ln2):
    ar3.append(ar2[k])
        

print([ar3[l] for l in range(len(ar3))])
for l in range(len(ar3)):
    print(ar3[l])

ln = len(ar3)
print(ln)
if (ln %2 == 0):
    med= (ar3[ln//2-1] + ar3[ln//2 ]) /2 
else :
    med = ar3[ln//2 ]
print(med)

print(np.median(ar3))