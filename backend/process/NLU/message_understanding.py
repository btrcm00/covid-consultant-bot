from backend.utils.utils import preprocess_message
from backend.config.regrex import sex_reg, age_reg, agree, disagree, check_has_symp, symptom_list, num_req, covid_infor_reg, medical_his_reg
from backend.config.constant import DISTRICT
from backend.process.PretrainedModel import PretrainedModel
from unidecode import unidecode
import regex as re
models = PretrainedModel()


def extract_information_message(message, last_intent):
    message = preprocess_message(message)
    # ---------- Check entity in message ----------- #
    entity_dict = {
        'age': '',
        'sex': '',
        'location': '',
        'symptoms': [],
        'medical_history': []
    }

    print("\t\t+++++++++ INTENT message +++++++++")
    intent = models.model_intent.predict(models.tfidf_intent.transform([message]))[0].lower()
    #intent sử dụng cho Request
    sub_intent = models.model_svm.predict(models.tfidf_svm.transform([message]))[0].lower()
    print('Intent:',intent,'Request intent:',sub_intent)



    print("\t\t+++++++++ Extract entity +++++++++")
    if last_intent.startswith('request_age') or re.search(age_reg, message):
        if re.search(r'\d+',message):
            age = re.findall(r'\d+', message)[0]
            if len(age)<=2 and age !='0':
                entity_dict['age'] = age
    
    if last_intent.startswith('request_sex') or any(re.search(sex_reg[i], message) for i in sex_reg):
        for reg in sex_reg:
            if re.search(sex_reg[reg], message):
                entity_dict['sex'] = reg
    
    if re.search(check_has_symp, message):
        for intensive in symptom_list:
            for sym in symptom_list[intensive]:
                if re.search(sym, message):
                    entity_dict['symptoms'].append(symptom_list[intensive][sym])

    if last_intent.startswith('request_location') or re.search(DISTRICT, message):
        location = re.findall(DISTRICT, message)
        if location:
            entity_dict['location'] = ''.join(unidecode(location[0]).split())

    for ele in medical_his_reg:
        if re.search(medical_his_reg[ele], message):
            entity_dict['medical_history'].append(ele)

    if intent == 'hello':
        pass
    if intent == 'request':
        intent += '_' + sub_intent
    elif intent == 'inform':
        temp = [i for i in entity_dict if entity_dict[i]]
        if temp:
            intent += '_' + temp[0]
    else:
        if re.search(r'v[a|á|â|ạ|ã|ả|â|ấ|ắ][c|t|g]\s*[x|s][i|y]n|vaccine', message):
            intent = 'request'
            sub_intent = 'vacxin'
        elif any(re.search(reg, message) for reg in covid_infor_reg):
            intent = 'request'
            sub_intent = 'covid_infor'
        elif re.search(num_req, message) and sub_intent != 'vacxin':
            intent = 'request'
            sub_intent = 'current_numbers'
        if re.search(r'v[a|á|â|ạ|ã|ả|â|ấ|ắ][c|t|g]\s*[x|s][i|y]n|vaccine', message):
            intent = 'request'
            sub_intent = 'vacxin'

        if last_intent.startswith('request'):
            intent = 'inform'
        elif intent=='ok' and any(entity_dict[i] for i in entity_dict):
            intent = 'inform'
        elif re.search(agree, message):
            intent = 'agree'
        elif re.search(disagree, message):
            intent = 'disagree' 

    return intent, entity_dict