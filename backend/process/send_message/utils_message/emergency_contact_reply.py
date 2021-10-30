from backend.config.constant import reply_text, contact_emergency, district_reg, MAP_TO_DISTRICT_HCM
import regex as re
from unidecode import unidecode

def emergency_contact_rep(text, pre_intent):
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
    contact = []
    reply = ''
    for ent in entity_lst:
        if ent in text:
            contact.append(ent)

    if len(contact)==0 and state["emergency_contact"]["who"]:
        contact = [state["emergency_contact"]["who"]]

    who_contact = '-'.join(unidecode(contact[0]).split()) if contact else ''
    for reg in MAP_TO_DISTRICT_HCM:
        if reg in text:
            text = re.sub(reg, MAP_TO_DISTRICT_HCM[reg], text)
    print(text)
    location = re.findall(district_reg, text)
    if not location and state["emergency_contact"]["location"]:
        location = [state["emergency_contact"]["location"]]
    elif location:
        state["emergency_contact"]["location"] = location[0]

    if len(contact)==0 and state["emergency_contact"]["who"] =="":
        reply = reply_text["request"]["emergency_contact"]["common"]
    elif len(location)==0:
        state["emergency_contact"]["who"] = contact[0]
        reply = reply_text['request']['emergency_contact'][who_contact]
    else:   
        print(['-'.join(unidecode(location[0]).split())])
        print(who_contact)
        pre_intent = 'Done-contact'
        reply = ['Bạn liên hệ theo một trong những số điện thoại dưới đây nha']
        reply.append(contact_emergency[who_contact]['-'.join(unidecode(location[0]).split())])
    
    return reply
    