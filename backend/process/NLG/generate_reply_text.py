import regex as re

def generate_reply_text(result, reply_text,response_knn):
    print('result nè',result)
    res_code = list(result.keys())[0]
    suggest_reply = ""
    check_end = False
    
    for idx, res in enumerate(res_code.split('-')):
        if idx>=1:
            suggest_reply += '*'

        if res == 'hello':
            suggest_reply += reply_text['hello']
        elif res.startswith('inform_first'):
            suggest_reply += reply_text[res.split('/')[0]].format(res.split('/')[1])
        elif res.startswith('inform_current_numbers'):
            loc,infected,recovered = res.split('+')[1:]
            suggest_reply += reply_text['inform_current_numbers'].format(loc,infected,recovered)
        elif 'inform_contact' in res:
            suggest_reply += reply_text['inform_contact']
            suggest_reply += "*image " + reply_text['contact_list']['tram-y-te'][res.split('+')[-1]]
        elif res.startswith('request_symptom'):
            suggest_reply += reply_text['request_symptom'][re.sub('request_symptom_', '', res)]
        elif res == 'reply_correct_text':
            a = response_knn.get(result[res]['choices'][0].lower(),'Chưa có dữ liệu cho câu hỏi này')
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
            suggest_reply += reply_text[res]
    #convert link
    out_text = suggest_reply.split(" ")
    for idx, text in enumerate(out_text):
        if "http" in text and (idx==0 or 'image' not in out_text[idx-1]):
            suggest_reply = re.sub(text, "<a target=\"_blank\" href=\"{}\">{}</a>".format(text,text), suggest_reply)
    
    return suggest_reply, result, check_end