# Initialize tracker with positive infinity
# import sys
# min_value = float('inf')

# numbers = [42, 17, 99, 8]
# print(min_value)
# for num in numbers:
#     if num < min_value:
#         min_value = num

# print(min_value)  # Outputs: 8

# # 1. Check the current digit limit (Default is 4300)
# print(sys.get_int_max_str_digits())

# # 2. Increase the limit if you expect massive numbers
# sys.set_int_max_str_digits(10000)

# # 3. Completely disable the limit (Use with caution)
# sys.set_int_max_str_digits(0)
# x = -2 ** 31 -1
# print(x)

import math
num  = 999887777
print(type(num))

strX = str(num)
rev = ''
for x in range(len(strX)):
    print(strX[x])
    rev = strX[x] + rev
    
print(rev)
    
lst = list(strX)
print(lst)

digit = ''
for i in lst:
    digit = str(i) + digit
dgt = int(digit)

if dgt > math.pow(2,31) -1:
    dgt = 0
    
print(dgt)
