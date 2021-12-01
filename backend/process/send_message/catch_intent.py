from backend.config.constant import MAP_TO_DISTRICT_HCM, DISTRICT
from backend.config.regrex import sex_reg, age_reg, check_has_symp, symptom_list, num_req, covid_infor_reg, w_ques
from backend.utils.utils import preprocess_message
import regex as re

from backend.process.send_message.utils_message.symptom_reply import symptom_rep
from backend.process.send_message.utils_message.vaccine_reply import vaccine_rep
from backend.process.send_message.utils_message.precaution_reply import precaution_rep
from backend.process.send_message.utils_message.medication_reply import medication_rep
from backend.process.send_message.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.send_message.utils_message.current_number_reply import current_numbers_rep
from backend.process.send_message.utils_message.common_info_reply import common_infor_rep

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()
from backend.config.config import get_config
config_app = get_config()

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

    if conversation_history:
        if 'request_age' in last_intent and intent != 'request':
            age = re.findall(r'\d+', message)
            if not age or (age and (len(age[0])>2 or age[0]=='0')):
                res['request_age-again'] = last_infor
                return res, intent, sub_intent
            else:
                last_infor['infor']['age'] = age[0]
                intent = 'inform'
            return symptom_rep(message, 'symptoms_have', last_intent, last_infor), intent, sub_intent
        elif 'request_sex' in last_intent and intent != 'request':
            check = False
            for s in sex_reg:
                if re.search(s, message):
                    check = True
                    last_infor['infor']['sex'] = sex_reg[s]
                    intent = 'inform'
                    break
            if not check:
                res['request_sex-again'] = last_infor
                return res, intent, sub_intent

            return symptom_rep(message, 'symptoms_have', last_intent, last_infor), intent, sub_intent        
        elif 'request_symptom' in last_intent:
            
            return symptom_rep(message, 'symptoms_have', last_intent, last_infor), intent, sub_intent
        elif ('request_location' in last_intent and intent!='request') or \
            (re.search(DISTRICT, message) and last_intent == 'inform_serious_prop'):
            intent = 'inform'
            return emergency_contact_rep(message, last_infor), intent, sub_intent

        elif last_infor['history']['state_vaccine']!='' :
            res = vaccine_rep(message, last_infor)
            return res, intent, sub_intent
        elif last_infor['history']['state_medication'] != '':
            if not 'request' in last_intent:
                res = medication_rep(message, last_infor, last_intent)
                return res, intent, sub_intent
            else:
                if 'rare' in last_intent:
                    symp_in_text = re.search(check_has_symp, message)
                    if symp_in_text:
                        intent = 'request'
                        sub_intent = 'symptom_have'
                    if re.search(num_req, message):
                        intent = 'request'
                        sub_intent = 'current_numbers'
                    t = symptom_rep(message, sub_intent, last_intent, last_infor)
                    last_intent = list(t.keys())[0]
                    last_infor = t[last_intent]
                    res = medication_rep(message, last_infor, last_intent)
                    return res, intent, sub_intent
        elif last_intent == 'request_covid_infor_chithi' and intent!='request':
            message += 'chỉ thị như nào'
            intent = 'inform'
            res_code = common_infor_rep(message)
            res[res_code] = last_infor
            return res, intent, sub_intent

    ''' print("\t\t+++++++++++++ check entity in message+++++++++++++++")
    symp_in_text = re.search(check_has_symp, message)
    if symp_in_text:
        intent = 'request'
        sub_intent = 'symptom_have'

    print("\t\t+++++++++++++Tự infer intent dùng regex (vì model chưa đủ tốt để predict)+++++++++++++++")
    if intent=='other' or intent == 'ok':
        if re.search(r'v[a|á|â|ạ|ã|ả|â|ấ|ắ][c|t|g]\s*[x|s][i|y]n|vaccine', message):
            intent = 'request'
            sub_intent = 'vacxin'
        elif any(re.search(reg, message) for reg in covid_infor_reg):
            intent = 'request'
            sub_intent = 'covid_infor'
        elif re.search(num_req, message) and sub_intent != 'vacxin':
            intent = 'request'
            sub_intent = 'current_numbers' '''
    
    if any(re.search(w_ques[i], message) for i in w_ques):
        intent = 'request'

    if intent =='hello':
        res['hello'] = last_infor
    elif intent == 'request':
        if 'diagnostic' in sub_intent:
            res = symptom_rep(message, sub_intent, last_intent, last_infor)
        elif 'contact' in sub_intent:
            res = emergency_contact_rep(message, last_infor)
        elif 'number' in sub_intent:
            res = current_numbers_rep(message, last_infor)
        else:
            res = common_infor_rep(message, models.corpus_knn, models.tfidf_knn, models.model_knn,last_infor)
    elif intent == 'ok':
        res['done'] = last_infor
    else:
        res['other'] = last_infor
    return res, intent, sub_intent