import regex as re

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()
mydb = models.myclient["chatbot_data"]
mycol_response_knn = mydb["data_response_knn"]
mycol_response = mydb["data_response"]

def get_response():
    cursor = mycol_response.find({})
    res={}
    for doc in cursor:
        res[doc['question']] = doc['answer']
    return res

def generate_reply_text(result):
    print('result nè',result)
    res_code = list(result.keys())[0]
    suggest_reply = ""
    reply_text = get_response()
    
    
    for idx, res in enumerate(res_code.split('-')):
        if idx>=1:
            suggest_reply += '*'

        if res.startswith('inform_first'):
            suggest_reply += reply_text[res.split('/')[0]].format(res.split('/')[1])
        elif res.startswith('inform_current_numbers'):
            loc,infected,caseToday,died = res.split('+')[1:]
            suggest_reply += reply_text['inform_current_numbers'].format(loc,infected,died,caseToday)
        elif 'inform_contact' in res:
            suggest_reply += reply_text['inform_contact']
            link = reply_text['contact_list']['tram-y-te'].get(res.split('+')[-1], 'none')
            if link == 'none':
                suggest_reply = reply_text['request_location_contact']
                result['request_location_contact'] = result.pop(res)
            else:
                suggest_reply += "*image " + link
        elif res.startswith('request_symptom'):
            suggest_reply += reply_text['request_symptom'][re.sub('request_symptom_', '', res)]
        elif res == 'reply_correct_text':
            
            reply = []
            document = mycol_response_knn.find_one({'question': result[res]['choices'][0]})
            if document:
                print(document)
                a = document['answer']
            else:
                a = 'Chưa có dữ liệu cho câu hỏi này'
            
            #a = response_knn.get(result[res]['choices'][0].lower(),'Chưa có dữ liệu cho câu hỏi này')
            if isinstance(a,list):
                suggest_reply += a[0]
                result[res]['choices'] = a[1]
                result['request_correct_text'] = result.pop(res)
            else:
                suggest_reply+=a
            if not suggest_reply:
                suggest_reply += "Chưa có dữ liệu câu trả lời cho câu hỏi này"
        elif res == 'request_correct_text':
            suggest_reply += 'Dạ ý bạn có phải là:'
        else:
            suggest_reply += reply_text.get(res, 'Bạn muốn hỏi gì ạ?')
    #convert link
    out_text = suggest_reply.split(" ")
    for idx, text in enumerate(out_text):
        if "http" in text and (idx==0 or 'image' not in out_text[idx-1]):
            suggest_reply = re.sub(text, "<a target=\"_blank\" href=\"{}\">{}</a>".format(text,text), suggest_reply)
    
    return suggest_reply, result