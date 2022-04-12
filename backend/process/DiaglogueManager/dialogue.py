import regex as re

from backend.config.constant import DISTRICT
from backend.process.DiaglogueManager.utils_message.diagnose_reply import symptom_rep
from backend.process.DiaglogueManager.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.DiaglogueManager.utils_message.current_number_reply import current_numbers_rep
from backend.process.DiaglogueManager.utils_message.common_infor_reply import common_infor_rep
from backend.process.config import PretrainedModel
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
                    "noi-man": "",
                    "tho-met": "",
                    "ho-ra-mau": "",
                    "dau-dau": ""
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
    if last_intent=='request_correct_text' and message in last_infor['choices']:
        return common_infor_rep(message, last_infor)
    #if last_intent!='request_correct_text':
    last_infor['choices']=[]
    
    if intent in ['hello']:
        res[intent] = last_infor
        
    elif intent in ['inform', 'ok', 'other']:
        print('haha',intent,last_intent )
        if 'request_symptom' in last_intent and 'request' not in intent:
            return symptom_rep(message, 'diagnostic', last_intent, last_infor)
        elif ('request_location' in last_intent and intent!='request') or \
            (re.search(DISTRICT, message) and last_intent == 'inform_serious_prop'):
            intent = 'inform'
            return emergency_contact_rep(message, last_infor)
        else:
            res[intent] = last_infor
            
    elif 'request' in intent:
        if 'diagnostic' in intent:
            res = symptom_rep(message, intent, last_intent, last_infor)
        elif 'contact' in intent:
            res = emergency_contact_rep(message, last_infor)
        elif 'number' in intent:
            res = current_numbers_rep(message, last_infor)
        else:
            res = common_infor_rep(message, last_infor)
    return res