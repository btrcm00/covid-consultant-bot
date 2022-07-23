import regex as re
from backend.config.config import Config
from backend.config.regrex import URL_REGEX


def generate_reply_text(result):

    mycol_response_knn = Config.mycol_response_knn #mydb["data_response_knn"]

    res_code = list(result.keys())[0]
    suggest_reply = ""
    reply_text = Config.reply_text #get_response(mycol_response)
    
    
    for idx, res in enumerate(res_code.split('-')):
        if idx>=1:
            suggest_reply += '*'

        if res.startswith('inform_first'):
            suggest_reply_temp = reply_text.get(res.split('/')[0], "")
            if not suggest_reply_temp:
                suggest_reply_temp = reply_text["do_not_have_response"]
            else:
                suggest_reply_temp = suggest_reply_temp.format(res.split('/')[1])
            
            suggest_reply += suggest_reply_temp

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
            
            document = mycol_response_knn.find_one({'question': result[res]['choices'][0]})
            if document:
                # print(22222222222222222222, document)
                a = document['answer']
            else:
                a = reply_text["do_not_have_response"]
            
            # print(1111111111111111111111111111111,a)
            if isinstance(a,list):
                suggest_reply += a[0]
                result[res]['choices'] = a[1]
                result['request_correct_text'] = result.pop(res)
            else:
                suggest_reply += a
            if not suggest_reply:
                suggest_reply += reply_text["do_not_have_response"]

        elif res == 'request_correct_text':
            suggest_reply += 'Dạ ý bạn có phải là:'
            
        else:
            suggest_reply += reply_text.get(res, 'Bạn muốn hỏi gì ạ?')
            
    #convert link
    out_text = suggest_reply.split(" ")
    for idx, text in enumerate(out_text):
        if re.search(URL_REGEX, text) and (idx==0 or 'image' not in out_text[idx-1]):
            # print(666666666666666666666, text, text in suggest_reply)
            suggest_reply = suggest_reply.replace(text, "<a target=\"_blank\" href=\"{}\">{}</a>".format(text,text))
            # print(55555555555555,suggest_reply, suggest_reply.replace(text, "<a target=\"_blank\" href=\"{}\">{}</a>".format(text,text)))
    
    return suggest_reply, result