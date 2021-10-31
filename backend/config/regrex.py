
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
    r't[ư|ứ|ú]c\s*ng[ư|ự|u]c': 'tuc-nguc',
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

age_reg = r'\d+'
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