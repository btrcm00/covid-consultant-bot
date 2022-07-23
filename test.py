def get_min_string(s:str, idx:int):
    print(f"Case #{idx}:", end = " ")
    str_ = ""
    
    for j in range(len(s)):
        if j>=len(s)-1:
            str_ += s[j]
        elif j<len(s)-1 and s[j] < s[j+1]:
            str_ += s[j]+s[j]
        elif s[j] == s[j+1]:
            k=j+1
            o=False
            while k<len(s)-1:
                if s[k] < s[k+1]:
                    str_ += s[j]+s[j]
                    o=True
                    break
                elif s[k] > s[k+1]:
                    break
                k+=1
            if not o:
                str_ += s[j]
        else:
            str_ += s[j]
            
    
    print(str_)
    

if __name__ =="__main__":
    num = int(input())
    
    tc = []
    for idx in range(num):
        tc.append(input())
        
    for idx, e in enumerate(tc):
        get_min_string(e, idx+1)
        
        
        