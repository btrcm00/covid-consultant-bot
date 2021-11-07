import regex as re
from backend.config.regrex import covid_infor_reg,w_ques


def common_infor_rep(text):
    print('\t\t------------------TƯ VẤN THÔNG TIN-------------------')
    sub_intent = ''
    res_code = 'inform_covid_infor_'

    for i in covid_infor_reg:
        if re.search(i, text):
            sub_intent = covid_infor_reg[i]
    
    if sub_intent=='chithi':
        if re.search(w_ques['what'], text):
            res_code += 'chithi_what'
        elif re.search(w_ques['how'], text):
            if not any(i in text for i in ['15', '16', '19']):
                res_code = 'request_covid_infor_chithi'
            else:
                res_code += 'chithi_how+' + [i for i in ['15', '16', '19'] if i in text][0]
        else:
            res_code += 'chithi_what'
    elif sub_intent=='testnhanh':
        if re.search(w_ques['what'], text):
            res_code += 'testnhanh_what'
        elif re.search(w_ques['how'], text):
            res_code += 'testnhanh_how'
        elif re.search(w_ques['where'], text):
            res_code += 'testnhanh_where'
        else:
            res_code += 'testnhanh_what'
    else:
        if re.search(w_ques['what'], text):
            res_code += 'common_what'
        elif re.search(w_ques['where'], text):
            res_code += 'common_where'
        elif re.search(w_ques['when'], text):
            res_code += 'common_when'
        else:
            res_code += 'common_what'
    
    return res_code