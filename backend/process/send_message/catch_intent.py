from backend.config.config import get_config
config_app = get_config()
from backend.config.constant import MAP_TO_DISTRICT_HCM, CODE_RETURN
from backend.config.regrex import sex_reg, age_reg, agree, disagree, check_has_symp, symptom_list
from backend.process.PretrainedModel import PretrainedModel
from backend.utils.utils import preprocess_message
import copy
import json
import regex as re
from backend.process.send_message.utils_message.symptom_reply import symptom_rep
from backend.process.send_message.utils_message.vaccine_reply import vaccine_rep
from backend.process.send_message.utils_message.precaution_reply import precaution_rep
from backend.process.send_message.utils_message.medication_reply import medication_rep
from backend.process.send_message.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.send_message.utils_message.current_number_reply import current_numbers_rep
from backend.process.send_message.utils_message.common_info_reply import common_infor_rep
models = PretrainedModel()

def catch_intent(self,message, conversation_history,conversation_message):
    message = preprocess_message(message)
    result = predict_message(self, message, conversation_history,conversation_message)
    return result

def predict_message(self, message, conversation_history, conversation_message):
    res = {}
    last_infor = {}
    last_intent = ''
    if conversation_history:
        last_intent = list(conversation_history[-1].keys())[0]
        last_infor = conversation_history[-1][last_intent]

    intent_history = [list(ele.keys())[0] for ele in conversation_history]
    print('\t\t+++++++++ INTENT HISTORY +++++++++')
    print(intent_history, last_intent)

    print("\t\t+++++++++ LAST INFOR in message +++++++++")
    if last_infor: print("last_infor: ", last_infor)
    else:
        last_infor = {
                'infor':{
                    'age' : 25 ,
                    'sex' : '' ,
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
                }
            }
    
    # ---------------TRANSFORM Q1 -> QUẬN 1, Q2 -> Quận 2, etc---------
    for key, value in MAP_TO_DISTRICT_HCM.items():
        if key in message:
            message = message.replace(key, value)
    
    # ---------- Check entity in message ----------- #
    print("\t\t+++++++++ INTENT message +++++++++")
    intent = models.model_intent.predict(models.tfidf_intent.transform([message]))[0].lower()
    #intent sử dụng cho Request
    sub_intent = models.model_svm.predict(models.tfidf_svm.transform([message]))[0].lower()
    print(intent,sub_intent)
    print("\t\t+++++++++++++++++++++++++++++++++++")
    check_sym_has = 'None'
    if conversation_history:
        if 'request_age' == last_intent:
            age = re.findall(r'\d{1,2}', message)
            if not age:
                res['request_age_again'] = last_infor
                return res
            else:
                last_infor['infor']['age'] = age[0]
        elif 'request_sex' == last_intent:
            check = False
            for s in sex_reg:
                if re.search(s, message):
                    check = True
                    last_infor['infor']['sex'] = sex_reg[s]
                    break
            if not check:
                res['request_sex_again'] = last_infor
                return res
            else:
                intent = 'request'
                sub_intent = 'symptom_have'
        elif 'request' in last_intent and 'symptom' in last_intent:
            symptom = re.sub(r'request_','',last_intent)
            if re.search(disagree, message):
                check_sym_has = 0
                for sym in symptom_list[symptom].values():
                    message += ' ' + sym

            intent = 'request'
            sub_intent = 'symptom_have'


    if intent =='hello':
        res['hello'] = last_infor
    elif intent == 'request':
        if 'symptom' in sub_intent:
            res = symptom_rep(message, sub_intent, models.reply_text, last_infor, check_sym_has)
        elif 'vaccine' in sub_intent:
            res = vaccine_rep(message, models.reply_text, last_infor)
        elif 'contact' in sub_intent:
            pass
        elif 'precaution' in sub_intent:
            pass
        elif 'current' in sub_intent:
            res = current_numbers_rep(message,models.reply_text, last_infor)
        elif 'medication' in sub_intent:
            pass
    else:
        res['other'] = last_infor
    return res