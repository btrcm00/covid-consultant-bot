import regex as re
import pickle
import json
import pandas as pd
import numpy as np
import os
from .load_model import tfidf_svm, model_svm, tfidf_intent, model_intent
from .models import Conversation, Client, Infor
from unidecode import unidecode

path = os.getcwd()
with open(path + '\\classifierbackend\\reply.json', encoding='utf-8') as f:
    reply_dic = json.load(f)
with open(path + '\\image\\emergycontact\\contact.json', encoding='utf-8') as f:
    contact_emergency = json.load(f)


state_conversation = 'Hello'
#state này để lưu những thông tin trong từng kịch bản
state = {
    "emergency_contact": {
        "who": "",
        "location": ""
    },
    "symptom": {},
    "precaution": {},
    "infor": {},
    "medication": {},
    "vacxin": {}
}
def symptom(text):
    entity_lst = ['ho', 'sốt', 'mệt mỏi', 'ho khan', 'đau họng', 'đau họng', 'đau nhức', 'tiêu chảy', 'mất vị giác', 'mất khứu giác', 'da nổi mẩn', 'tấy đỏ', 'tím tái', 'khó thở', 'mất khả năng nói hoặc cử động', 'tức ngực']
    entity_in_text = []
    for ent in entity_lst:
        if ent in text:
            entity_in_text.append(ent)

def common_information(text):
    pass

def precaution(text):
    pass

def medication(text):
    pass

def vacxin(text):
    pass

def emergency_contact(text):
    """
    Kịch bản:
    - Khi khách hàng request liên lạc với các trung tâm y tế, ...
    - Nếu đầu vào câu khách nhắn hỏi liên lạc trạm y tế hay trạm y tế lưu động nhưng chưa biết địa chỉ của bệnh nhân
        => hỏi bệnh nhân ở quận nào
        - Nếu bệnh nhân báo quận thì gửi hình ảnh các số liên lạc cho bệnh nhân
    - Nếu đầu vào có đủ các thông tin, ví dụ "em ở quận X thì liên hệ trạm y tế nào vậy ạ"
        => gửi hình ảnh sđt cho bệnh nhân
    - Nếu câu hỏi mang tính chung chung
        => gửi danh sách các cách thức liên hệ với bệnh nhân + request thêm bệnh nhân muốn hỏi cụ thể chỗ nào.
    """
    entity_lst = ['tổ phản ứng nhanh', 'trạm y tế lưu động', 'trạm y tế']
    localtion_reg = r'[quâậan]+\s*([1-9]+|b[i|ì]nh\s*th[a|ạ]nh|t[a|â]n\s*ph[u|ú]|b[i|ì]nh\s*t[a|â]n|b[i|ì]nh\s*ch[a|á]nh|nh[a|à]\s*b[e|è]|g[o|ò]\s*v[a|á|ấ|â]p|ph[u|ú]\s*nhu[a|ạ|â|ậ]n|t[a|â]n\s*b[i|ì][|n]h|th[u|ủ]\s[d|đ][u|ú|ư|ứ]c|c[a|à|ầ|â]n\s*gi[o|ơ|ờ]|c[u|ủ]\schi|h[o|ó]c\s*m[o|ô]n)'
    contact = []
    reply = ''
    for ent in entity_lst:
        if ent in text:
            contact.append(ent)

    if len(contact)==0 and state["emergency_contact"]["who"]:
        contact = [state["emergency_contact"]["who"]]

    location = re.findall(localtion_reg, text)
    if not location and state["emergency_contact"]["location"]:
        location = [state["emergency_contact"]["location"]]
    elif location:
        state["emergency_contact"]["location"] = location[0]

    if len(contact)==0 and state["emergency_contact"]["who"] =="":
        reply = reply_dic["Request"]["emergency_contact"]["common"]
    elif len(location)==0:
        state["emergency_contact"]["who"] = contact[0]
        reply = 'Bạn ở quận mấy vậy ạ?'
    else:
        print(['-'.join(unidecode(location[0]).split())])
        print('-'.join(unidecode(contact[0]).split()))
        reply = ['Bạn liện hệ theo một trong những số điện thoại dưới đây nha']
        reply.append(contact_emergency['-'.join(unidecode(contact[0]).split())]['-'.join(unidecode(location[0]).split())])
    
    return reply
    
def reply(text):
    #intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']
    #intent cho câu của bệnh nhân
    intent = model_intent.predict(tfidf_intent.transform([text]))[0]
    #intent sử dụng cho Request
    intent_request = model_svm.predict(tfidf_svm.transform([text]))[0]
    global state_conversation
    print(intent, intent_request)
    response = ""

    #Nếu bệnh nhân request intent nào thì chuyển state hội thoại sang hướng đó
    if intent == 'Request':
        state_conversation = intent_request

    if intent in ['Request', 'Inform']:
        if state_conversation == 'emergency_contact':
            response = emergency_contact(text)
        elif state_conversation == 'symptom':
            pass
        elif state_conversation == 'infor':
            pass
        elif state_conversation == 'precaution':
            pass
        elif state_conversation == 'medication':
            pass
        elif state_conversation == 'vacxin':
            pass
    else:
        response = reply_dic[intent]

    return response