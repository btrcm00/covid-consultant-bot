from backend.config.regrex import covid_infor_reg,w_ques
from backend.config.config import Config


def common_infor_rep(text,last_infor):
    print('\t\t------------------TƯ VẤN THÔNG TIN-------------------')
    res_code = 'request_correct_text'
    threshold = 0.85
    res = {}
    
    trans = Config.tfidf_knn.transform([text])
    distance, idx_choices = Config.model_knn.kneighbors(trans)
    distance = 1 - distance[0]
    if distance[0] > threshold:
        res_code = 'reply_correct_text'
        choices = [Config.corpus_knn[idx_choices[0][0]]]
        print([Config.corpus_knn[i] for i in idx_choices[0]][:2])
    else:
        res_code = 'request_correct_text'
        choices = [Config.corpus_knn[i] for i in idx_choices[0]][:2]
    
    res[res_code] = last_infor
    res[res_code]['choices'] = choices
    return res