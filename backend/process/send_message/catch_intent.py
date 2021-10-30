from backend.config.config import get_config
config_app = get_config()
from backend.config.constant import MAP_TO_DISTRICT_HCM, CODE_RETURN
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
    if conversation_history:
        for ele in CODE_RETURN:
            if any(ele in key for key in conversation_history[-1]):
                pass

    intent_history = [list(ele.keys())[0] for ele in conversation_history]
    print('\t\t+++++++++ INTENT HISTORY +++++++++')
    print(intent_history)

    print("\t\t+++++++++ LAST INFOR in message +++++++++")
    if last_infor: print("last_infor: ", last_infor)
    
    # ---------------TRANSFORM Q1 -> QUẬN 1, Q2 -> Quận 2, etc---------
    for key, value in MAP_TO_DISTRICT_HCM.items():
        if key in message:
            message = message.replace(key, value)
    
    # ---------- Check entity in message ----------- #
    print("\t\t+++++++++ INTENT message +++++++++")
    intent = models.model_intent.predict(models.tfidf_intent.transform([message]))[0].lower()
    #intent sử dụng cho Request
    intent_request = models.model_svm.predict(models.tfidf_svm.transform([message]))[0].lower()
    print(intent,intent_request)
    print("\t\t+++++++++++++++++++++++++++++++++++")

    if conversation_history:
        pass
    
    if intent in ['other', 'hello']:
        res={
            'rep_hello': {
                'infor':{
                    'name': 'Công Minh' ,
                    'age' : 21 ,
                    'sex' : 'nam' ,
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
                }
            }
        }
    if intent == 'request':
        if 'symptom' in intent_request:
            res = symptom_rep(message, models.reply_text)
        elif 'vaccine' in intent_request:
            pass
        elif 'contact' in intent_request:
            pass
        elif 'precaution' in intent_request:
            pass
        elif 'current' in intent_request:
            pass
        elif 'medication' in intent_request:
            pass
    return res