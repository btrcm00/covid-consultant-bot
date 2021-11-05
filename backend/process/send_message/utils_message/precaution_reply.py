import regex as re
from backend.config.regrex import precaution_reg, w_ques

def precaution_rep(text):
    """
    Cách ly 38
    Giám sát thân nhiệt 44
    Sử dụng khẩu trang 45
    Rửa tay 49
    Vệ sinh, dinh dưỡng 
    """
    print('\t\t------------------THÔNG TIN PHÒNG NGỪA-------------------')
    sub_pre = 'common'
    w_code = 'common'
    for i in precaution_reg:
        if re.search(precaution_reg[i], text):
            sub_pre = i
    
    for i in w_ques:
        if re.search(w_ques[i], text):
            w_code = i
    if sub_pre == 'common': w_code = 'common'
    res_code = 'inform_precaution+' + sub_pre + '+' + w_code

    return res_code    