str = "abcd"

def permute(s):
    if len(s) <= 1:
        return [s]

    result = []

    for i in range(len(s)):
        current = s[i]
        print(s[:i])
        print(s[i+1:])
        remaining = s[:i] + s[i+1:]

        for p in permute(remaining):
            result.append(current + p)

    return result
        
    
def main():
    result =  permute(str)
    for perm in result:
        print(perm)
     
if __name__ == '__main__':
    main()  
