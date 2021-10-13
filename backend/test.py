import regex as re

localtion_reg = r'(ho|s[ô|ố|ó]t|m[ệ|ẹ|e|ê]t\s*m[o|ỏ]i|[đ|d]au\s*h[o|ọ]ng|kh[o|ó]\s*th[ơ|ở|ỏ]|[đ|d]au\s*nh[ư|ú|ứ]c|ti[ê|e]*u\s*ch[a|ả]y|\
                    |m[a|ấ|â|á]t\s*v[i|ị]\s*gi[a|á]c|n[ô|ổ|ỏ]i\s*m[a|ả|ẩ|â]n|t[i|í]m\s*t[a|á]i|t[ư|ứ|u|ú]c\s*ng[ụ|ự|ư|u]c)'
print(re.findall(localtion_reg, 'em bị khó thở với đau họng đau nhức tiu chảy mất vị giác tím tái á'))