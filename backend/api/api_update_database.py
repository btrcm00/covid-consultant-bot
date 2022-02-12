import pickle
import sys
import json
sys.path.append('.')
from backend.config.config import get_config
config_app = get_config()
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel(config_app['models_chatbot'])


def update_database(data):
# ---------------- 4.BOT ---------------- #
    mydb = models.myclient["chatbot_data"]
    mycol = mydb["data_response"]
    col = []
    all_doc = [doc['question'] for doc in list(mycol.find({}))]
    for key,value in data.items():
        if key not in all_doc:
            col.append({
                "question": key,
                "answer": value
            })
    print('numer of new document',len(col))
    if col:
        tmp = mycol.insert_many(col)
    
    return 'done'
