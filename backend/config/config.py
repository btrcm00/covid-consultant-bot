import yaml
import pickle
import json
import pymongo
import regex as re

def get_config():
    with open('app.yml', encoding='utf-8') as cfgFile:
        config_app = yaml.safe_load(cfgFile)
        # cfgFile.close()
    return config_app


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
    config_app = get_config()
    tfidf_svm, model_svm = pickle.load(open(config_app['models_chatbot']['model_load_text']['model'], 'rb'))
    tfidf_intent, model_intent = pickle.load(open(config_app['models_chatbot']['model_load_text']['intent_model'], 'rb'))
    corpus_knn,model_knn,tfidf_knn = pickle.load(open(config_app['models_chatbot']['model_load_text']['knn_model'], 'rb'))
    
    __myclient = pymongo.MongoClient(config_app['mongodb']['link_db_server'])
    database = __myclient["chatbot_data"]
    mycol_response_knn = database["data_response_knn"]
    mycol_response = database["data_response"]
    intent_db = database["data_intent"]
    reply_text = get_response(mycol_response)

    short_word_file = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['short_word_file'], encoding='utf-8')
    short_word_dic = json.load(short_word_file)

    teencode_re_file = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['teencode_regex'], encoding='utf-8')
    teencode_re_dic = json.load(teencode_re_file)

    single_word_dic = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['single_word_dic'], 'r', encoding='utf-8')
    single_word_dic_line = single_word_dic.readlines()
    single_word_dic = [re.sub('\n', '', s) for s in single_word_dic_line]

    vowel_file = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['vowel'], encoding='utf-8')
    vowel_dic = json.load(vowel_file)

    fi = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['telex_fault'], encoding='utf-8')
    complex_telex = json.load(fi)

    f2 = open(config_app['chatbot_api']['general_chatbot']['spell_corection']['tudien_don'], 'r', encoding='utf-8')
    dictionary = json.load(f2)
    
    current_number_url = config_app['chatbot_api']['general_chatbot']['current_number_url']
    chatbot_password = config_app['chatbot_api']['password']['insert_data']
    
    logging = config_app['log']['app']
