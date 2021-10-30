import json
import sys
import pickle
import pymongo
from os import path
import re


from backend.config.config import get_config
config_app = get_config()

class PretrainedModel:
    _instance = None
    def __new__(cls, cfg=None, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PretrainedModel, cls).__new__(cls, *args, **kwargs)
            
            # 1. Load response data trong send-message
            json_data = open(cfg['models_chatbot']['response_data'], 'rb')
            cls.reply_text = json.loads(json_data.read())

            # 2. Model load text
            cls.tfidf_svm, cls.model_svm = pickle.load(open(cfg['model_load_text']['model'], 'rb'))
            cls.tfidf_intent, cls.model_intent = pickle.load(open(cfg['model_load_text']['intent_model'], 'rb'))

            #3. Load monggodb
            cls.myclient = pymongo.MongoClient(config_app['mongodb']['link_db_server'])

            short_word_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['short_word_file'], encoding='utf-8')
            cls.short_word_dic = json.load(short_word_file)

            teencode_re_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['teencode_regex'], encoding='utf-8')
            cls.teencode_re_dic = json.load(teencode_re_file)

            single_word_dic = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['single_word_dic'], 'r', encoding='utf-8')
            single_word_dic_line = single_word_dic.readlines()
            cls.single_word_dic = [re.sub('\n', '', s) for s in single_word_dic_line]

            vowel_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['vowel'], encoding='utf-8')
            cls.vowel_dic = json.load(vowel_file)

            fi = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['telex_fault'], encoding='utf-8')
            cls.complex_telex = json.load(fi)

            f2 = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['tudien_don'], 'r', encoding='utf-8')
            cls.dictionary = json.load(f2)
        return cls._instance
