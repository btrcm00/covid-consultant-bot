import regex as re
from backend.config.constant import DISTRICT
from backend.process.DiaglogueManager.utils_message.symptom_reply import symptom_rep
from backend.process.DiaglogueManager.utils_message.vaccine_reply import vaccine_rep
from backend.process.DiaglogueManager.utils_message.precaution_reply import precaution_rep
from backend.process.DiaglogueManager.utils_message.medication_reply import medication_rep
from backend.process.DiaglogueManager.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.DiaglogueManager.utils_message.current_number_reply import current_numbers_rep
from backend.process.DiaglogueManager.utils_message.common_infor_reply import common_infor_rep

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

def dialogue(message,last_intent, entity_dict, last_infor, intent):
    new_last_infor = update_slots(entity_dict, last_infor)
    result = predict_reply(message,last_intent, new_last_infor, intent)
    return result

def update_slots(entity_dict, last_infor):
    if not last_infor:
        last_infor = {
                'infor':{
                    'age' : '' ,
                    'sex' : '' ,
                    'address': '',
                },
                'symptom': {
                    "sot": "",
                    "met-moi": "",
                    "ho": "",
                    "kho-tho": "",
                    "tuc-nguc": "",
                    "mat-kha-nang": "",
                    "dau-hong": "",
                    "dau-nhuc": "",
                    "tieu-chay": "",
                    "mat-vi-giac": "",
                    "tim-tai": "",
                    "noi-man": ""
                },
                'diagnose':{
                    "tree_degree":"",
                    "normal_symptom": "",
                    "serious_symptom": "",
                    "covid_test": "",
                    "result_test": "",
                    "been_covidarea": "",
                    "close_f": ""
                },
                'history':{
                'cothai':'',
                'gan':'',
                'diung':'',
                'mantinh':'',
                'datiemvaccine':'',
                'vaccinedatiem':'',
                'f':'',
                'ruoubia':'',
                'chongchidinh':'',
                'state_vaccine':'',
                'state_medication':''
                }
            }
    # Cập nhật các entity mới nhất vào slots của hội thoại
    for i in entity_dict:
        if not entity_dict[i]:
            continue
        if i in ['age', 'sex', 'address']:
            last_infor['infor'][i] = entity_dict[i]
        elif i == 'symptom':
            for j in entity_dict[i]:
                last_infor['symptom'][j] = 1 
        elif i == 'medical_history':
            for j in entity_dict[i]:
                last_infor['history'][j] = 1 
    print("last infor after update", last_infor)
    return last_infor

def predict_reply(message, last_intent, last_infor, intent):
    res={}
    if intent in ['other','hello', 'ok', 'done']:
        res[intent] = last_infor
    elif intent in ['inform']:
        if 'request_symptom' in last_intent:
            res = symptom_rep(message, intent, last_intent, last_infor)
        elif 'request_location' in last_intent or \
            (re.search(DISTRICT, message) and last_intent == 'inform_serious_prop'):
            res = emergency_contact_rep(message, last_infor)
    elif 'request' in intent:
        if 'current_numbers' in intent:
            res = current_numbers_rep(intent, last_infor)
        elif 'covid_infor' in intent:
            res = common_infor_rep(text)
        elif 'symptom' in intent:
            res = symptom_rep(message, intent, last_intent, last_infor)
        elif 'vacxin' in intent:
            res = vaccine_rep(message, last_infor)
        elif 'contact' in intent:
            res = emergency_contact_rep(message, last_infor)
        elif 'precaution' in intent:
            res_code = precaution_rep(message)
            res[res_code] = last_infor
    print(intent)
    return res