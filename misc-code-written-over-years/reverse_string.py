#Simple code to reverse an array. This will not work to reverse string. It is immutable
str = ['a', 'b', 'c','d', 'e']
len = len(str)
ln = len//2
l =0
while l < ln:
    tmp = str[l]
    str[l] = str[len-1-l]
    str[len-l-1 ]= tmp
    l += 1

print(str)    
     