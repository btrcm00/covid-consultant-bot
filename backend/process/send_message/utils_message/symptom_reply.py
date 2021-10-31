from backend.config.regrex import symptom_list
from unidecode import unidecode
import regex as re

def symptom_rep(text, sub_intent, reply_text, last_infor, check_has='None'):
    res = {}
    res_code = ''
    request_lst =  [i for i in last_infor['infor'] if not last_infor['infor'][i]] + list(symptom_list.keys())
    if 'infor' in sub_intent:
        res_code = 'inform_symptoms_info'
    else:
        for intensity_sym in symptom_list:
            for sym in symptom_list[intensity_sym]:
                if re.search(sym, text):
                    symp = symptom_list[intensity_sym][sym]
                    last_infor['symptom'][symp] = 0 if check_has==0 else 1
                    if intensity_sym in request_lst:
                        request_lst.remove(intensity_sym)
                
        
        if request_lst:
            res_code = 'request_' + request_lst[0]
        else:
            res_code = 'inform_need_symptom_predict_model'
    res[res_code] = last_infor
    return res
    