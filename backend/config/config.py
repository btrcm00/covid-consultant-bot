import os
import pickle
import json
import pymongo
import regex as re


from backend.config.common_keys import *

def get_response(mycol_response):
    cursor = mycol_response.find({})
    res={}
    for doc in cursor:
        res[doc['question']] = doc['answer']
    return res


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    svm_file = os.getenv(SVM_FILE)
    tfidf_svm, model_svm = pickle.load(open(svm_file, 'rb'))
    
    intent_file = os.getenv(INTENT_MODEL_FILE)
    tfidf_intent, model_intent = pickle.load(open(intent_file, 'rb'))
    
    knn_file = os.getenv(KNN_MODEL_FILE)
    corpus_knn,model_knn,tfidf_knn = pickle.load(open(knn_file , 'rb'))
    
    database_uri = os.getenv(DATABASE_URI)
    __myclient = pymongo.MongoClient(database_uri)
    database = __myclient["chatbot_data"]
    mycol_response_knn = database["data_response_knn"]
    mycol_response = database["data_response"]
    intent_db = database["data_intent"]
    reply_text = get_response(mycol_response)

    short_word_file = os.getenv(SHORT_WORT_FILE)
    short_word_dic = json.load(open(short_word_file, "r", encoding="utf8"))

    teencode_re_file = os.getenv(SINGLE_RE_FILE)
    teencode_re_dic = json.load(open(teencode_re_file, "r", encoding="utf8"))

    single_word_dic = open(os.getenv(SINGLE_WORD_DICT), 'r', encoding='utf-8')
    single_word_dic_line = single_word_dic.readlines()
    single_word_dic = [re.sub('\n', '', s) for s in single_word_dic_line]

    vowel_file = os.getenv(VOWEL_FILE)
    vowel_dic = json.load(open(vowel_file, "r", encoding="utf8"))

    fi = os.getenv(TELEX_FAULT)
    complex_telex = json.load(open(fi, "r", encoding="utf8"))

    f2 = os.getenv(TUDIEN_DON)
    dictionary = json.load(open(f2, "r", encoding="utf8"))
    
    current_number_url = os.getenv(CURRENT_CASE_CRAWL_API)
    chatbot_password = os.getenv(DATA_ACCESS_PASSWORD)
    
    logging = "app.log"
    
    service_host = os.getenv(SERVICE_HOST)
    service_port = os.getenv(SERVICE_PORT)