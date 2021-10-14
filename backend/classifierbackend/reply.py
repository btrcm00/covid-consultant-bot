import regex as re
import pickle
import urllib.request, json 
import pandas as pd
import numpy as np
from .load_model import tfidf_svm, model_svm, tfidf_intent, model_intent
from .models import Conversation, Client, Infor
from unidecode import unidecode

from .constant import *


state_conversation = 'Hello'
pre_intent = ""
check = ''
#state này để lưu những thông tin trong từng kịch bản
state = {
    "infor_patient": {
        "name": "",
        "age": "",
        "sex": "",
        "phone": ""
    },
    "emergency_contact": {
        "who": "",
        "location": ""
    },
    "symptom": {
        "usually": {
            "sot": "",
            "met-moi": "",
            "ho": ""
        },
        "serious": {
            "kho-tho": "",
            "tuc-nguc": "",
            "mat-kha-nang": ""
        },
        "rarely": {
            "dau-hong": "",
            "dau-nhuc": "",
            "tieu-chay": "",
            "mat-vi-giac": "",
            "tim-tai": "",
            "noi-man": ""
        }
    },
    "precaution": {},
    "infor": {},
    "medication": {},
    "vacxin": {}
}
def symptom(text, intent = 'Request'):
    global pre_intent
    entity_lst = ['ho', 'sốt', 'mệt mỏi', 'đau họng', 'đau nhức', 'tiêu chảy', 'mất vị giác', 'nổi mẩn'
                    , 'tím tái', 'khó thở', 'mất khả năng', 'tức ngực']
    
    entity_in_text = re.findall(symptom_reg, text)
    severity = {
        sev: 1 if any([state['symptom'][sev][i] for i in state['symptom'][sev]]) \
                        else (0 if any([state['symptom'][sev][i]==0 for i in state['symptom'][sev]]) else "")
        for sev in ['serious', 'rarely', 'usually']
    }
    severity = {**severity, **{'age':state['infor_patient']['age'], 'sex': state['infor_patient']['sex']}}
    print('symptoms:',entity_in_text)
    for symp in entity_in_text:
        for ele in state['symptom']:
            if '-'.join(unidecode(symp).split()) in state['symptom'][ele].keys():
                state['symptom'][ele]['-'.join(unidecode(symp).split())] = 1
                
    for ele in state['symptom']:
        if any([state['symptom'][ele][i] for i in state['symptom'][ele]]):
            if ele in severity:
                severity[ele] = 1

    if intent == 'OK':
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
        return reply_dic['Request']['symptom_have'][pre_intent]
    
    pre_intent == 'Done-Symptom'
    if severity['serious']==1 or all([severity[ele] for ele in severity if ele != 'serious']):
        return reply_dic['Request']['symptom_have']['high_prop']
    
    return reply_dic['Request']['symptom_have']['low_prop']

def common_information(text):
    pass

def precaution(text):
    pass

def medication(text):
    pass

ques={"time":["lâu","giãn","2","hai","gian","atras","sino","pfizer",'mode'],
    "f1":["f1"],
    "f0":["f0"],
    "women":["thai"],
    "old":["già"],
    "injected":["xong","về"],
    "condition":["nhiêu","điều","đang dùng","nền"]
    }
def timevaccine(cus,intent):
    global check
  
    num=0
    vaccine=["atraszenenca","sinopharm","pfizer",'moderna']
    if check=='time':
        for ele2 in cus.split():
            for x in  vaccine:
                if ele2.lower() in x:
                    return reply_dic['Request']['vacxin']['time'][num]
                    break
                num=num+1
            num=0
        check='time_next'
        return "cho hỏi bạn đã tiêm vacxin loại nào"
        
    if check=='time_next':
        for x in vaccine:
            if cus.lower() in x:
                break
            num=num+1
        
    return reply_dic['Request']['vacxin']['time'][num]

def womenn(cus,intent):
    global check
    if check=="women":
        check="women_next"
        return "Phụ nữ "+reply_dic['Request']['vacxin']['old'][0]
    if check=="women_next":
        if intent=="Ok":
            return reply_dic['Request']['vacxin']['old'][1]
        else:
            return reply_dic['Request']['vacxin']['women'][0]

def oldd(cus,intent):
    global check
    if check=="old":
        check="old_next"
        return "Người già " +reply_dic['Request']['vacxin']['old'][0]
    if check=="old_next":
        if intent=="Ok":
            return reply_dic['Request']['vacxin']['old'][1]
        else:
            return reply_dic['Request']['vacxin']['old'][2]
def injecc(cus,intent):
    global check
    if check=="injected":
        check="injected_next"
        return "Bạn có hay uống rượu bia hay có tiền sử bệnh gan không ạ"
    if check=="injected_next":
        if intent=='Ok':
            return reply_dic['Request']['vacxin']['injected'][1] 
        else:
            return reply_dic['Request']['vacxin']['injected'][0]
def condition(cus,intent):
    global check
    if check=="condition":
        check="condition_next1"
        return "Bạn "+ reply_dic['Request']['vacxin']['old'][0]
    if check=="condition_next1":
        if intent=='Ok':
            return reply_dic['Request']['vacxin']['condition'][1]
        check="condition_next2"
        return "Bạn có bị bệnh mãn tính hay dị ứng gì không ạ"
    if check=="condition_next2":
        if intent=='Ok':
            return reply_dic['Request']['vacxin']['condition'][2]
        else:
            return reply_dic['Request']['vacxin']['condition'][0]
def vaccine(cus,intent):
    global check
    for ele in ques:
        for ele2 in cus.split():
            if ele2.lower() in ques[ele]:
                check=ele
    
    if check=='f1':
        #return
        return reply_dic['Request']['vacxin']['f1'][0]
    elif check=='f0':
        #return
        return reply_dic['Request']['vacxin']['f0'][0] 
    elif check=='old'or check=='old_next':
        #return
        return oldd(cus,intent)
        
    elif check=='women'or check=='women_next':
        #return
        return womenn(cus,intent)
    elif check=='time' or check=='time_next':
        return timevaccine(cus)
    elif check=="injected" or check=="injected_next":
        return injecc(cus,intent)
    elif check=="condition" or check=="condition_next1"  or check=="condition_next2":
        return condition(cus,intent)
    else:
        return reply_dic['Request']['vacxin']['common']

def emergency_contact(text):
    #----------------------------------------------#
    # Kịch bản:
    # - Khi khách hàng request liên lạc với các trung tâm y tế, ...
    # - Nếu đầu vào câu khách nhắn hỏi liên lạc trạm y tế hay trạm y tế lưu động nhưng chưa biết địa chỉ của bệnh nhân
    #     => hỏi bệnh nhân ở quận nào
    #     - Nếu bệnh nhân báo quận thì gửi hình ảnh các số liên lạc cho bệnh nhân
    # - Nếu đầu vào có đủ các thông tin, ví dụ "em ở quận X thì liên hệ trạm y tế nào vậy ạ"
    #     => gửi hình ảnh sđt cho bệnh nhân
    # - Nếu câu hỏi mang tính chung chung
    #     => gửi danh sách các cách thức liên hệ với bệnh nhân + request thêm bệnh nhân muốn hỏi cụ thể chỗ nào.
    #----------------------------------------------#
    entity_lst = ['tổ phản ứng nhanh', 'trạm y tế lưu động', 'trạm y tế']
    
    global pre_intent
    contact = []
    reply = ''
    for ent in entity_lst:
        if ent in text:
            contact.append(ent)

    if len(contact)==0 and state["emergency_contact"]["who"]:
        contact = [state["emergency_contact"]["who"]]

    who_contact = '-'.join(unidecode(contact[0]).split()) if contact else ''
    location = re.findall(district_reg, text)
    if not location and state["emergency_contact"]["location"]:
        location = [state["emergency_contact"]["location"]]
    elif location:
        state["emergency_contact"]["location"] = location[0]

    if len(contact)==0 and state["emergency_contact"]["who"] =="":
        reply = reply_dic["Request"]["emergency_contact"]["common"]
    elif len(location)==0:
        state["emergency_contact"]["who"] = contact[0]
        reply = reply_dic['Request']['emergency_contact'][who_contact]
    else:   
        print(['-'.join(unidecode(location[0]).split())])
        print(who_contact)
        pre_intent = 'Done-contact'
        reply = ['Bạn liên hệ theo một trong những số điện thoại dưới đây nha']
        reply.append(contact_emergency[who_contact]['-'.join(unidecode(location[0]).split())])
    
    return reply
    
def current_numbers(text):
    #----------------------------------------------#
    # - Bắt địa chỉ trong câu của bệnh nhân (tỉnh thành)
    # - Nếu bắt được thì sẽ reply theo tỉnh thành đó
    # - Nếu không thì mặc định là số liệu cho cả nước VN.
    #----------------------------------------------#
    
    data = {}
    with urllib.request.urlopen("https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true") as url:
        data = json.loads(url.read().decode())
    infected = data['infected']
    recovered = data['recovered']
    died = data['died']
    loc = 'Việt Nam'
    text = re.sub(r'hcm|sài gòn|tphcm|tp\.hcm|sg', 'tp. hồ chí minh', text)
    text = re.sub(r'huế', 'thừa thiên huế', text)
    text = re.sub(r'vtau|vung\s*tau|vũng tàu|vt', 'bà rịa – vũng tàu', text)

    for pro in province_lst:
        if pro.lower() in text:
            loc,infected,died = [(ele['name'],ele['cases'], ele['death']) for ele in data['locations'] if ele['name'].lower() == pro.lower()][0]
            recovered = 0

    res = reply_dic['Request']['current_numbers']
    return [res[0].format(loc, infected, recovered, died), res[1]]

def reply(text):
    #intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']
    #intent cho câu của bệnh nhân
    intent = model_intent.predict(tfidf_intent.transform([text]))[0]
    #intent sử dụng cho Request
    intent_request = model_svm.predict(tfidf_svm.transform([text]))[0]
    global state_conversation
    global pre_intent
    print(intent, intent_request)
    
    response = ""

    #Nếu bệnh nhân request intent nào thì chuyển state hội thoại sang hướng đó
    if intent in ['Request', 'Inform']:
        state_conversation = intent_request
    elif intent == 'OK':
        if state_conversation == 'symptom_have' and not pre_intent == 'Done-Symptom':
            return symptom(text, intent)
        elif state_conversation == 'emergency_contact' and not pre_intent == 'Done-contact':
            return emergency_contact(text)

    if intent in ['Request', 'Inform']:
        if state_conversation == 'emergency_contact':
            response = emergency_contact(text)
        elif state_conversation == 'symptom_have':
            response = symptom(text)
        elif state_conversation == 'precautions':
            pass
        elif state_conversation == 'medication':
            pass
        elif state_conversation == 'vacxin':
            response = vaccine(text, intent)
        elif state_conversation == 'current_numbers':
            response = current_numbers(text)
        else:
            return reply_dic["Request"][state_conversation]
    else:
        response = reply_dic[intent]
    print(response)
    return response