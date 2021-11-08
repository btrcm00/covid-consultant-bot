from backend.utils.utils import preprocess_message
from backend.config.regrex import *
from backend.config.constant import DISTRICT
from backend.process.PretrainedModel import PretrainedModel
from unidecode import unidecode

import regex as re
models = PretrainedModel()
def extract_information_message(message):
    message = preprocess_message(message)
    
    entity_dict = extract_entity_message(message)
    intent = extract_intent_message(message, entity_dict)
        
    return intent, entity_dict

def extract_entity_message(message):
    entity_dict = {
        'age': '',
        'sex': '',
        'location': '',
        'symptoms': [],
        'medical_history': []
    }
    print("\t\t+++++++++ Extract entity +++++++++")
    if re.search(age_reg, message) and not re.search(DISTRICT, message):
        if re.search(r'\d+',message):
            age = re.findall(r'\d+', message)[0]
            if len(age)<=2 and age !='0':
                entity_dict['age'] = age
    
    if any(re.search(sex_reg[i], message) for i in sex_reg):
        for reg in sex_reg:
            if re.search(sex_reg[reg], message):
                entity_dict['sex'] = reg
    
    if re.search(check_has_symp, message):
        for intensive in symptom_list:
            for sym in symptom_list[intensive]:
                if re.search(sym, message):
                    entity_dict['symptoms'].append(symptom_list[intensive][sym])

    if re.search(DISTRICT, message):
        location = re.findall(DISTRICT, message)
        if location:
            entity_dict['location'] = ''.join(unidecode(location[0]).split())

    for ele in medical_his_reg:
        if re.search(medical_his_reg[ele], message):
            entity_dict['medical_history'].append(ele)

    return entity_dict

def extract_intent_message(message, entity_dict):
    print("\t\t+++++++++ INTENT message +++++++++")
    intent = models.model_intent.predict(models.tfidf_intent.transform([message]))[0].lower()
    #intent sử dụng cho Request
    sub_intent = models.model_svm.predict(models.tfidf_svm.transform([message]))[0].lower()
    print('Intent:',intent,'- Request intent:',sub_intent)
    
    print("\t\t+++++++++ Extract intent +++++++++")
    if intent == 'hello':
        pass
    elif intent == 'request' or any(re.search(w_ques[i], message) for i in w_ques):
        intent = 'request_' + sub_intent
        if sub_intent == 'precautions':
            t = [i for i in precaution_reg if re.search(precaution_reg[i], message)]
            intent += '_' + t[0] if t else ''
    elif intent == 'inform' or any(entity_dict[i] for i in entity_dict):
        temp = [i for i in entity_dict if entity_dict[i]]
        if temp:
            intent = 'inform_' + temp[0]
        else:
            intent = 'inform'
    else:
        if re.search(disagree, message):
            intent = 'disagree'
        elif re.search(agree, message):
            intent = 'agree'
        elif re.search(done, message):
            intent = 'done'
        else:
            intent = 'other'
    
    return intent

