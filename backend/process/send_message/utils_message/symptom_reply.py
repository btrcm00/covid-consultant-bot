from backend.config.regrex import symptom_list
from unidecode import unidecode
import regex as re

def symptom_rep(text, sub_intent, last_req, last_infor):
    res = {}
    res_code = ''
    print('\t\t------------------TƯ VẤN TRIỆU CHỨNG-------------------')
    if 'info' in sub_intent:
        res_code = 'inform_symptoms_info'
    else:
        lst_sym = []
        if last_req and 'symptom' in last_req and 'request' in last_req and '/' not in last_req:
            last_req = re.sub('request_','',last_req)
            for sym in symptom_list[last_req]:
                if re.search(sym, text):
                    assign = 1
                else: assign = 0
                symp = symptom_list[last_req][sym]
                if last_infor['symptom'][symp]=='':
                    last_infor['symptom'][symp] = assign

        else:
            for intensity_sym in symptom_list:
                for sym in symptom_list[intensity_sym]:
                    if re.search(sym, text):
                        lst_sym.append(re.findall(sym, text)[0])
                        symp = symptom_list[intensity_sym][sym]
                        if last_infor['symptom'][symp]=='':
                            last_infor['symptom'][symp] = 1
            
        request_lst =  [i for i in last_infor['infor'] if not last_infor['infor'][i] and i!='address'] \
                    + [i for i in symptom_list if any(last_infor['symptom'][j]=='' for j in symptom_list[i].values())]
                    
        print('REQUEST_LIST', request_lst)
        if request_lst:
            if lst_sym:
                res_code += 'inform_first_symptom/' + ', '.join(lst_sym) + '-'
            res_code += 'request_' + request_lst[0]
        else:
            count = 0
            for i in last_infor['symptom']:
                if last_infor['symptom'][i] == 1:
                    count += 1
            if count/12 > 0.5:
                res_code +=  'inform_high_prop-diagnose'
            else:
                res_code += 'inform_low_prop-diagnose'
    res[res_code] = last_infor
    return res
    