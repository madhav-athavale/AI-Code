from itertools import islice

with open("claims.txt", "r") as f:
    lines = iter(f)
    for line in lines:
       
        if "Medical" in line:
            for nxt in islice(lines, 8):
                print(nxt.strip())
    
    
    
    #lines= f.readlines()

# lines_iter = iter(lines)
# for line in lines_iter:
    
#     if "Medical" in line:
#         print(line)
#         print(next(lines_iter,None))
#     if ("Date of service") in line:
#         print(line)
#         print(next(lines_iter,None))
#     # if ("Provider") in line:
#     #     print(line)
#     # if ("Total you may be billed") in line:
#     #     print("Total you may be billed")
#     # prev = line