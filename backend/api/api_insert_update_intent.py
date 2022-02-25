import pickle
import sys
import json
sys.path.append('.')
from backend.config.config import get_config
config_app = get_config()
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel(config_app['models_chatbot'])
import pandas as pd

# def update_data(data):
# # ---------------- 4.BOT ---------------- #
#     mydb = models.myclient["chatbot_data"]
#     mycol = mydb["data_response_knn"]
#     col = []
#     all_doc = [doc['question'] for doc in list(mycol.find({}))]
#     for idx in range(len(data['question'])):
#         if data['question'][idx] not in all_doc:
#             col.append({
#                 "question": data['question'][idx],
#                 "answer": data['answer'][idx],
#             })
#     print('number of new document',len(col))
#     if col:
#         tmp = mycol.insert_many(col)
    
#     return 'done'

def insert_data(data):
    mydb = models.myclient["chatbot_data"]
    mycol = mydb["data_intent"]
    col = []
    # all_doc = [doc['text'] for doc in list(mycol.find({}))]
    for idx in range(len(data['text'])):
        # if data['text'][idx] not in all_doc:
        #     col.append({
        #         "text": data['text'][idx],
        #         "intent": data['intent'][idx],
        #         "sub_intent": data['sub_intent'][idx] if data['sub_intent'] else 'None'
        #     })
        mycol.update({'text': data['text'][idx]}, 
                     {'$set': {'intent': data['intent'][idx], "sub_intent": data['sub_intent'][idx]}}, upsert= True)
    # print('number of new document',len(col))
    # if col:
    #     tmp = mycol.insert_many(col)
    
    return 'done'


if __name__ == "__main__":
    data = pd.read_excel(open("D:/212/thesis/DCLV/backend/data/data_model/data_chatbot.xlsx", 'rb'))
    # for i in range(data.shape[0]):
    data = {
        'text': data['text'].values,
        'intent': data['intent'].values,
        'sub_intent': data['sub intent'].values
    }
    insert_data(data)