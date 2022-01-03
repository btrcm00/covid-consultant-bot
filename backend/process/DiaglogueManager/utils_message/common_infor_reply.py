import regex as re
from backend.config.regrex import covid_infor_reg,w_ques
from backend.config.config import get_config
config_app = get_config()
import pickle


def common_infor_rep(text,last_infor):
    print('\t\t------------------TƯ VẤN THÔNG TIN-------------------')
    sub_intent = ''
    res_code = 'request_correct_text'
    threshold = 0.85
    res = {}
    corpus_knn,model_knn,tfidf_knn = pickle.load(open(config_app['models_chatbot']['model_load_text']['knn_model'], 'rb'))
    trans = tfidf_knn.transform([text])
    distance, idx_choices = model_knn.kneighbors(trans)
    distance = 1 - distance[0]
    if distance[0] > threshold:
        res_code = 'reply_correct_text'
        choices = [corpus_knn[idx_choices[0][0]]]
        print([corpus_knn[i] for i in idx_choices[0]][:2])
    else:
        res_code = 'request_correct_text'
        choices = [corpus_knn[i] for i in idx_choices[0]][:2]
    
    res[res_code] = last_infor
    res[res_code]['choices'] = choices
    return res