
import pandas as pd

from os import path

import sys
sys.path.append('..')

usual_symptom = {
    r's[ô|ố|ó|o]t' : 'sot',
    r'ho': 'ho',
    r'm[ê|ệ|e|ẹ]t\s*m[o|ỏ]i': 'met-moi'
}
serious_symptom = {
    r'kh[o|ó]\s*th[o|ơ|ở]': 'kho-tho',
    r't[ư|ứ|ú|u]c\s*ng[ư|ự|u]c': 'tuc-nguc',
    r'm[â|ấ|a]t\s*kh[a|ả]\s*n[a|ă][|n]g': 'mat-kha-nang'
}
rare_symptom = {
    r'[d|đ]au\s*h[o|ọ][|n]g': 'dau-hong',
    r'[d|đ]au\s*nh[ứ|ư|u]c': 'dau-nhuc',
    r'ti[e|ê|]u\s*ch[a|ả]y': 'tieu-chay',
    r'm[a|ấ|â]t\s*v[i|ị]\s*gi[á|a]c': 'mat-vi-giac',
    r't[í|i]m\s*t[a|á]i': 'tim-tai',
    r'n[ô|ổ|o]i\s*m[â|ẩ|a]n': 'noi-man'
}
symptom_list = {
    'usual_symptom':usual_symptom,
    'serious_symptom':serious_symptom,
    'rare_symptom':rare_symptom
}
check_has_symp = '|'.join([i for j in symptom_list for i in symptom_list[j]])


age_reg = r'\d{1,2}'
sex_reg = {
    r'nam|trai|[d|đ][a|à]n\s*[o|ô][n|]g': 'male',
    r'n[ữ|ư]|[d|đ][a|à]n\s*b[a|à]|ph[u|ụ]\s*n[ư|ữ]|g[a|á]i': 'female'
}

agree = r'\b([o|ô|0|u]k[a-zA-Z]*|oce|[d|z][a|ạ|à][a-zA-Z]*|c[o|ó]|ola|[u|ừ|o|ù][m|h|k|a]*|[o|ờ]|v[a|â|ầ]n*g|v[a|â|ầ]ng*|[d|đ][u|ú]n*g|[đ|d]c|[d|đ][u|ư][ơ|o|ợ]c|r[ồ|u|ù|o|ô]i|tks|thank|thanks|c[a|ả]m\s*[o|ơ]n|đ[o|ồ]ng\s*[y|ý]|dr)\b'
disagree = r'\b(th[u|ô|o][i|y]*|(hix)+|kh[o|ô]ng|ko|k\s(\s)*|(hu)+|tks|c[a|ả|á|u|ủ]m\s*[o|ơ]n|thanks|thank|thank\s*you|ti[e|ế|ê]c|ch[a|ậ]t)\b'



### TIME
pt_time_pre = r'sáng|trưa|tối|chiều|ng[à|a]y|h[ô|u|o]m|mùng|tuần|bữa'
pt_day = r'nay|mai|kia|mốt'
pt_hour = r'\d{1,2}((\-|\s|_|\sđến\s|\shoặc\s)\d{1,2})*\s*(h|tiếng|g(iờ)*|\'|phút|giây)(\s*\d{1,2}[\'|p(hút)*]*)*(\s(sáng|trưa|tối|chiều))*'
pt_date = r'(t(h[ứ|ư|u])*\s*\d((\-|\s|_|\sđến\s|\shoặc\s)\d)*|cn)(\s{})*'.format(pt_time_pre)
pt_num_pre = r'\d+((\-|\s|_|\sđến\s|\shoặc\s)\d+)*\s*({})'.format(pt_time_pre)
pt_pre_day_date = r'((\d+|{})\s*)*({})\s({}|{}|qua|tr(ướ)*c)'.format(pt_time_pre,pt_time_pre,pt_day,pt_date)
pt_time_phrase = r'(gi|h)ờ\shành\sch[á|í]nh(ngày\sthường)*'
pt_spec_date = r'({})'.format(pt_time_pre) + r'\s\d{1,2}((\s|-|\/)\d{1,2}((\s|-|\/)\d{2,4})*)*'
pt_time_summary = r'\b({}|{}|{}|{}|{}|{}|sáng|trưa|tối|mai|mốt|chủ\snhật)\b'.format(pt_pre_day_date, pt_num_pre, pt_date, pt_hour,pt_time_phrase, pt_spec_date)
###-------------------------------------------


num_req = r's[o|ô|ố]\s*ca|(bao)?\s*nhi[|e|ê]u|t[i|ỉ|y|ỷ]\s*l[e|ê|ệ]\s*(nh[i|ĩ][|e|ễ|ê]m|m[ắ|a|ă]c)'



ques={"time":r'l[a|â]u|[g|d][i][a|ã|â][n|m][g|]|2|\sh[a|â]i',
        "f1":r'f\s*(1|m+[o|ô|ộ]t)',
        "f0":r'f\s*(0|kh[o|ô|ộ]n)',
        "women":r'(ma[n|]g|c[ó|o])?\s*thai',
        "old":r'[d|g][i][a|à]',
        "register":r'[d|đ][a|â|á|ă|à|ã|ắ|ặ|ấ]n|[k|c][i|y|í|ý]',
        "injected":r'[x|s][o|ô|ơ][n|m][g]|[v|d][ê|e|è|ề|é|iề|ie|iê|iè]',
        "condition":r'nh[i|ê|e|è|ề|é|iề|ie|iê|iè]u|[d|đ][i|ì][e|ề|ê|]u\s*k[i|ị][e|ẹ|ê|ệ]n|[n|m][ê|e|è|ề]n',
        "number":r'm[a|á|ấ|â]y\s*lo[a|ạ]i|(bao)?\s*nhi[|e|ê]u'
}
vaccine=[r'a[s|t]t[r|]a',r'[s|x]i[n|m]o',r'[p|f][f|]i[z|d]er',r'[m|n][o|ô|ơ][|d]er', r'sputni[t|k]', r'[v|z][i|e|ê][r|d][ô|o]']
gan=r'\b(g[a|á|â|ạ|ă][m|n])\b'
man=r'\b(m[a|ã|â|ẫ|ẵ][m|n])\b'
di=r'\b([d|g][i|y|ỵ|ị|í])\b'
bia=r'\b([b|p]i[a]|r[u|ư|ụ|i|ị][ơ|o|]u)\b'


covid_infor_reg = {
    r'ch[i|ỉ]\s*th[i|ị]' : 'chithi',
    r'test|tes|tét|tet\s*(nha[n|]h|covi[d|t]|cô vít)': 'testnhanh',
}

w_ques = {
    r'what': r'l[à|a]\s*([g|d][i|ì]|sao)|l[a|à]m\s*([d|g][i|ì|]|chi)',
    r'how' : r'(th[e|ê|ế]|nh[ư|u])\s*n[a|à]o|b[ă|ằ|a][n|]g\s*c[a|á]ch\s*n[a|à]o|l[à|a]m\s*sao',
    r'where': r'[o|ơ|ở]\s*[d|đ][a|â|ă]u|ch[o|ô|ỗ]\s*n[a|à]o',
    r'when': r'khi\s*n[a|à]o|l[u|ú]c\s*n[a|à]o|bao\s*l[a|â]u|(m[â|ấ|á|a]y|bao\s*nhi[ê|e|]u)\s*ng[a|à]y',
    r'who' : r'ai|nh[u|ư|ữ][n|]g\s*ai|ng[u|ư][o|ơ|ờ]i\s*n[a|à]o'
}

precaution_reg = {
    r'cachly': r'c[á|a][c|]h\s*l[y|i]',
    r'thannhiet': r'([d|g][i|][a|á]m\s*s[a|á]t|[d|đ]o)\s*th[a|â]n\s*nhi[e|ẹ|ê|ệ]t',
    r'khautrang': r'kh[a|â|ẩ|ả]u\s*(ch|tr)a[n|]g',
    r'ruatay': r'r[u|ư|ủ|ử]a\s*tay',
    r'vesinh': r'(v[e|ê|ẹ|ệ]\s*[x|s]i[n|]h|di[n|]h\s*d[u|ư][o|ơ|ỡ][n|]g)'
}

medication_reg={
    "damac_covid_chuaco_trieuchung": r'ch[ă|a]m|u[o|ố]ng|d[u|ù|ụ]ng\s*thu[o|ố]c',
    "location_medicine":r'thu[o|ố]c.*(mua|ph[a|á]t).*(ở|n[ơ|o]i|ch[ỗ|o]|đ[â|a]u)|(ở|n[ơ|o]i|ch[ỗ|o]|đ[â|a]u).*(mua|ph[a|á]t).*thu[o|ố]c',
    "buy_medicine":r'thuốc.*(mua|ph[a|á]t)|(mua|ph[a|á]t).*thuốc',
    "spo":r'spo|[đ|d]o.*[o|ô]\s*x[y|i]',
    "device":r'thi[e|ê|é|ế]t\s*b[ị|i]|d[ụ|u]ng\s*c[ụ|u]|v[ậ|a]t\s*d[ụ|u]ng|má[y|i]',
    "5k": r'5k',
    "binhoxy":r'b[i|ì]nh.*[o|ô]\s*x[y|i]'
}

cachdo=r'c[á|a]ch\s*d[u|ù|ụ]ng|s[ử|ư|u]\s*d[u|ù|ụ][n|]g|c[á|a]ch\s*[d|đ]o|[d|đ]o\s*th[e|ế]|d[u|ù|ụ]ng\s*[d|đ]o'
f0_macbenh=r'f\s*(1|m[o|ô|ộ]t)|b[e|ệ][n|]h'
daubung=r'[d|đ]a[u|o]\s*b[u|ụ]ng'