from backend.config.constant import symptom_reg
import regex as re
from unidecode import unidecode

def symptom_rep(text, reply_text):
    entity_in_text = [sym[0] for sym in re.findall(symptom_reg, text)]
    print('symptoms:',entity_in_text)
    severity = {
        sev: 1 if any([state['symptom'][sev][i] for i in state['symptom'][sev]]) \
                        else (0 if any([state['symptom'][sev][i]==0 for i in state['symptom'][sev]]) else "")
        for sev in ['serious', 'rarely', 'usually']
    }
    severity = {**severity, **{'age':state['infor_patient']['age'], 'sex': state['infor_patient']['sex']}}
    
    for symp in entity_in_text:
        for ele in state['symptom']:
            if '-'.join(unidecode(symp).split()) in state['symptom'][ele].keys():
                state['symptom'][ele]['-'.join(unidecode(symp).split())] = 1
                
    for ele in state['symptom']:
        if any([state['symptom'][ele][i] for i in state['symptom'][ele]]):
            if ele in severity:
                severity[ele] = 1

    if intent == 'ok':
        print(pre_intent)
        if pre_intent == 'age':
            severity['age'] = re.findall(r'(\d+)', text)[0]
            state['infor_patient']['age'] = severity['age']
        elif pre_intent == 'sex':
            severity['sex'] = re.findall(r'(nam|n[ư|ữ])', text)[0]
            state['infor_patient']['sex'] = severity['sex']
        elif 'không' in text:
            severity[pre_intent] = 0
            for ele in state['symptom'][pre_intent]:
                state['symptom'][pre_intent][ele] = 0
        elif 'có' in text:
            severity[pre_intent] = 1
            for ele in state['symptom'][pre_intent]:
                state['symptom'][pre_intent][ele] = 1

    if any([severity[ele]=="" for ele in severity]):
        pre_intent = [i for i in severity if severity[i]==""][0]
        return reply_text['request']['symptoms_have'][pre_intent]
    
    pre_intent == 'Done-Symptom'
    if severity['serious']==1 or all([severity[ele] for ele in severity if ele != 'serious']):
        return reply_text['request']['symptoms_have']['high_prop']
    
    return reply_text['request']['symptoms_have']['low_prop']