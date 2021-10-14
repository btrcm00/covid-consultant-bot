import regex as re
import os
import json

path = os.getcwd()
with open(path + '\\classifierbackend\\reply.json', encoding='utf-8') as f:
    reply_dic = json.load(f)
with open(path + '\\image\\emergycontact\\contact.json', encoding='utf-8') as f:
    contact_emergency = json.load(f)


district_reg = r'[quâậan]+\s*([1-9]+|b[i|ì]nh\s*th[a|ạ]nh|t[a|â]n\s*ph[u|ú]|b[i|ì]nh\s*t[a|â]n|b[i|ì]nh\s*ch[a|á]nh|nh[a|à]\s*b[e|è]|g[o|ò]\s*v[a|á|ấ|â]p|ph[u|ú]\s*nhu[a|ạ|â|ậ]n|t[a|â]n\s*b[i|ì][|n]h|th[u|ủ]\s[d|đ][u|ú|ư|ứ]c|c[a|à|ầ|â]n\s*gi[o|ơ|ờ]|c[u|ủ]\schi|h[o|ó]c\s*m[o|ô]n)'

symptom_reg = r'(ho|s[ô|ố|ó]t|m[ệ|ẹ|e|ê]t\s*m[o|ỏ]i|[đ|d]au\s*h[o|ọ]ng|kh[o|ó]\s*th[ơ|ở|ỏ]|[đ|d]au\s*nh[ư|ú|ứ]c|ti[ê|e]*u\s*ch[a|ả]y|\
                |m[a|ấ|â|á]t\s*v[i|ị]\s*gi[a|á]c|n[ô|ổ|ỏ]i\s*m[a|ả|ẩ|â]n|t[i|í]m\s*t[a|á]i|t[ư|ứ|u|ú]c\s*ng[ụ|ự|ư|u]c)'

province_lst = ["Bắc Giang","Bắc Kạn","Cao Bằng","Hà Giang","Lạng Sơn","Phú Thọ","Quảng Ninh","Thái Nguyên","Tuyên Quang","Lào Cai","Yên Bái","Điện Biên","Hòa Bình","Lai Châu","Sơn La","Bắc Ninh","Hà Nam","Hải Dương","Hưng Yên","Nam Định","Ninh Bình","Thái Bình","Vĩnh Phúc","Hà Nội","Hải Phòng","Hà Tĩnh","Nghệ An","Quảng Bình","Quảng Trị","Thanh Hóa","Thừa Thiên Huế","Đắk Lắk","Đắk Nông","Gia Lai","Kon Tum","Lâm Đồng","Bình Định","Bình Thuận","Khánh Hòa","Ninh Thuận","Phú Yên","Quảng Nam","Quảng Ngãi","Đà Nẵng","Bà Rịa–Vũng Tàu","Bình Dương","Bình Phước","Đồng Nai","Tây Ninh","TP. Hồ Chí Minh","An Giang","Bạc Liêu","Bến Tre","Cà Mau","Đồng Tháp","Hậu Giang","Kiên Giang","Long An","Sóc Trăng","Tiền Giang","Trà Vinh","Vĩnh Long","Cần Thơ"] 