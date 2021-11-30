import regex as re

def generate_reply_text(self, result, reply_text,response_knn):
    res_code = list(result.keys())[0]
    suggest_reply = ""
    check_end = False
    
    for idx, res in enumerate(res_code.split('-')):
        if idx>=1:
            suggest_reply += '*'

        if res == 'hello':
            suggest_reply += reply_text['hello']
        if res.startswith('inform_first'):
            suggest_reply += reply_text[res.split('/')[0]].format(res.split('/')[1])
        if res.startswith('inform_current_numbers'):
            loc,infected,recovered = res.split('+')[1:]
            suggest_reply += reply_text['inform_current_numbers'].format(loc,infected,recovered)
        if res in ['request_age','request_sex', 'inform_symptoms_info',
                        'inform_low_prop', 'inform_high_prop','request_location_contact', 'done',
                         'again','diagnose','incomming', 'request_covid_infor_chithi','inform_serious_prop']:
            suggest_reply += reply_text[res]
        if res.startswith('inform_covid_infor'):
            if res.startswith('inform_covid_infor_chithi_how'):
                suggest_reply += reply_text['inform_covid_infor_chithi_how'][res.split('+')[-1]]
            else:
                suggest_reply += reply_text[res]
        if res.startswith('inform_precaution'):
            suggest_reply += reply_text[res.split('+')[0]][res.split('+')[1]][res.split('+')[2]]
        if 'inform_contact' in res:
            suggest_reply += reply_text['inform_contact']
            suggest_reply += "*image " + reply_text['contact_list']['tram-y-te'][res.split('+')[-1]]
        if 'vaccine' in res and not 'medication' in res:
            suggest_reply += reply_text[res]
        if 'medication' in res:
            suggest_reply += reply_text['inform_medication'][re.sub('medication_', '', res)]
        if res.startswith('request_symptom'):
            suggest_reply += reply_text['request_symptom'][re.sub('request_symptom_', '', res)]
        if res == 'other':
            result['request_correct_text'] = result.pop('other')
            suggest_reply += reply_text['request_correct_text'].format(option_1='số ca nhiễm nhiêu á', option_2='triệu chứng covid là gì á')
        if res == 'reply_correct_text':
            suggest_reply += response_knn.get(result[res]['choices'][0].lower(),'')
        if res == 'request_correct_text':
            suggest_reply += 'Dạ ý bạn có phải là:'
    #convert link
    out_text = suggest_reply.split(" ")
    for idx, text in enumerate(out_text):
        if "http" in text and (idx==0 or 'image' not in out_text[idx-1]):
            suggest_reply = re.sub(text, "<a target=\"_blank\" href=\"{}\">{}</a>".format(text,text), suggest_reply)
    
    return suggest_reply, result, check_end