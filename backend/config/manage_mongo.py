import pymongo

import sys
sys.path.append('.')
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()
import base64
import gridfs
import io
from PIL import Image

def insert_mongo(mycol, result={}, input_data={}, 
        ls_product={}, suggest_reply="",product_ID=""):
    
    # 3. Insert data
    data = {
        "mid": input_data["mid"],
        "SenderId": input_data["sender_id"],
        "RecipientId": input_data["recipient_id"],
        "bot_suggest": suggest_reply,
        "admin_reply": ""
    }

    print('-------- RESULT IN MANAGE_MONGO --------')
    print(result)
    print('---------------------------------------')
    
    if result:

        cur_intent = [ele for ele in result.keys()]
        if cur_intent and cur_intent[0] == 'rep_feedback':
            data['last_conversation'] = result
            data['message_text'] = 'GỬI ẢNH PHẢN HỒI CHO LỖI GIAO HÀNG CỦA SHOP'
        else:
            if ls_product:
                data['last_conversation'] = result
                data['message_text'] = 'GỬI ẢNH của ' + ls_product[product_ID]
            else:
                data['last_conversation'] = result
                data['message_text'] = input_data['text']
    else:
        data['last_conversation'] = {'dontunderstand': None}
        data['message_text'] = 'GỬI ẢNH KHÔNG PHẢI CỦA HUME'
    print(f"Data:{data}")
    tmp = mycol.insert_one(data)
    print('INSERT TO MONGO')
