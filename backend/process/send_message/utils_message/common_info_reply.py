import regex as re
from backend.config.regrex import covid_infor_reg,w_ques


def common_infor_rep(text, corpus,tfidf, model,pca,last_infor):
    print('\t\t------------------TƯ VẤN THÔNG TIN-------------------')
    sub_intent = ''
    res_code = 'request_correct_text'
    threshold = 0.7
    res = {}
    
    trans = pca.transform(tfidf.transform([text]))
    distance, idx_choices = model.kneighbors(trans)
    distance = 1 - distance[0]
    if distance[0] > 0.8:
        res_code = 'reply_correct_text'
        choices = [corpus[idx_choices[0][0]]]
    else:
        res_code = 'request_correct_text'
        choices = [corpus[i] for i in idx_choices[0]][:2]
    
    res[res_code] = last_infor
    res[res_code]['choices'] = choices
    return res