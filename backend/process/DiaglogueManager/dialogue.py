import regex as re

from backend.process.DiaglogueManager.utils_message.symptom_reply import symptom_rep
from backend.process.DiaglogueManager.utils_message.vaccine_reply import vaccine_rep
from backend.process.DiaglogueManager.utils_message.precaution_reply import precaution_rep
from backend.process.DiaglogueManager.utils_message.medication_reply import medication_rep
from backend.process.DiaglogueManager.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.DiaglogueManager.utils_message.current_number_reply import current_numbers_rep
from backend.process.DiaglogueManager.utils_message.common_infor_reply import common_infor_rep

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

def dialogue(last_intent, entity_dict, last_infor, intent):
    new_last_infor = update_slots(entity_dict, last_infor)
    result = predict_reply(last_intent, new_last_infor, intent)
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

def predict_reply(last_intent, last_infor, intent):
    res={}
    if intent == ['other','hello']:
        res[intent] = last_infor
    if intent in ['inform','ok']:
        pass
    if 'request' in intent:
        if 'current_numbers' in intent:
            res = current_numbers_rep(intent, last_infor)
        if 'covid_infor' in intent:
            res = common_infor_rep(text)
    return res