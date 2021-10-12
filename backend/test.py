import regex as re

localtion_reg = r'[quâậan]+\s*([1-9]+|b[i|ì]nh\s*th[a|ạ]nh|t[a|â]n\s*ph[u|ú]|b[i|ì]nh\s*t[a|â]n|b[i|ì]nh\s*ch[a|á]nh|nh[a|à]\s*b[e|è]|g[o|ò]\s*v[a|á|ấ|â]p|ph[u|ú]\s*nhu[a|ạ|â|ậ]n|t[a|â]n\s*b[i|ì][|n]h|th[u|ủ]\s[d|đ][u|ú|ư|ứ]c|c[a|à|ầ|â]n\s*gi[o|ơ|ờ]|c[u|ủ]\schi|h[o|ó]c\s*m[o|ô]n)'
    
print(re.findall(localtion_reg, 'em ở qạn 12as '))