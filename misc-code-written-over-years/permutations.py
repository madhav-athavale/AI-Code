orig = "ABC"

def permute(inp,suffix):
    ln = len(inp)
   
    print( inp + suffix)
    suffix = inp[0] + suffix 
    inp = inp[1:]
    
    if  inp == "":
        return
    permute(inp,"")
        
 
permute(orig,"")
