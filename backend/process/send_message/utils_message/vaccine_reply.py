from backend.config.constant import reply_text

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
                    return reply_text['request']['vacxin']['time'][num]
                    break
                num=num+1
            num=0
        check='time_next'
        return "Bạn muốn hỏi về vacxin loại nào ạ?"
        
    if check=='time_next':
        for x in vaccine:
            if cus.lower() in x:
                break
            num=num+1
        
    return reply_text['request']['vacxin']['time'][num]

def womenn(cus,intent):
    global check
    if check=="women":
        check="women_next"
        return "Phụ nữ "+reply_text['request']['vacxin']['old'][0]
    if check=="women_next":
        if intent=="ok":
            return reply_text['request']['vacxin']['old'][1]
        else:
            return reply_text['request']['vacxin']['women'][0]

def oldd(cus,intent):
    global check
    if check=="old":
        check="old_next"
        return "Người già " +reply_text['request']['vacxin']['old'][0]
    if check=="old_next":
        if intent=="ok":
            return reply_text['request']['vacxin']['old'][1]
        else:
            return reply_text['request']['vacxin']['old'][2]
def injecc(cus,intent):
    global check
    if check=="injected":
        check="injected_next"
        return "Bạn có hay uống rượu bia hay có tiền sử bệnh gan không ạ"
    if check=="injected_next":
        if intent=='ok':
            return reply_text['request']['vacxin']['injected'][1] 
        else:
            return reply_text['request']['vacxin']['injected'][0]
def condition(cus,intent):
    global check
    if check=="condition":
        check="condition_next1"
        return "Bạn "+ reply_text['request']['vacxin']['old'][0]
    if check=="condition_next1":
        if intent=='ok':
            return reply_text['request']['vacxin']['condition'][1]
        check="condition_next2"
        return "Bạn có bị bệnh mãn tính hay dị ứng gì không ạ"
    if check=="condition_next2":
        if intent=='ok':
            return reply_text['request']['vacxin']['condition'][2]
        else:
            return reply_text['request']['vacxin']['condition'][0]
def vaccine_rep(cus,intent):
    global check
    for ele in ques:
        for ele2 in cus.split():
            if ele2.lower() in ques[ele]:
                check=ele
    
    if check=='f1':
        #return
        return reply_text['request']['vacxin']['f1'][0]
    elif check=='f0':
        #return
        return reply_text['request']['vacxin']['f0'][0] 
    elif check=='old'or check=='old_next':
        #return
        return oldd(cus,intent)
        
    elif check=='women'or check=='women_next':
        return womenn(cus,intent)
    elif check=='time' or check=='time_next':
        return timevaccine(cus, intent)
    elif check=="injected" or check=="injected_next":
        return injecc(cus,intent)
    elif check=="condition" or check=="condition_next1"  or check=="condition_next2":
        return condition(cus,intent)
    else:
        return reply_text['request']['vacxin']['common']
