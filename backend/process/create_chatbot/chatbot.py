import os
import json
import requests
import re
import sys
from datetime import datetime

sys.path.append("..")
from backend.config.config import get_config
from backend.process.send_message.catch_intent import catch_intent
from backend.process.send_message.generate_reply_message.generate_reply_text import generate_reply_text
from backend.utils.spell_corrector import correct_sent

from backend.utils.error_handler import error_handler
config_app = get_config()

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['NO_PROXY'] = '127.0.0.1'
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

class CovidBot():
    def __init__(self):
        pass
    def reply(self,input_data):
        # get time start
        time_start = datetime.now()
        time_start = time_start.strftime("%Y-%m-%d")
        # 1. Get in Mongo
        try:
            mydb = models.myclient["chatbot_data"]
            mycol = mydb["chatbot_conversations"]
            message = input_data['text']
            conversation_history = []
            conversation_message = []
            last_suggest = []
            print("\t\t-------START RETRIEVAL--------")
            for ele in mycol.find({'SenderId': input_data['sender_id']}):
                conversation_history.append(ele['last_conversation'])
                conversation_message.append(ele['message_text'])
                last_suggest.append(ele['bot_suggest'])

            # sửa lỗi chính tả
            print("RAW MESSAGE:", message)
            
            if re.search(r'\bc[òo]n\s*k\b', message):
                message = re.sub(r'\bc[òo]n\s*k\b', 'còn ko', message)
            message = correct_sent(message)
            print("CORRECTED MESSAGE:", message)
            print('Historyyy',conversation_history)
            # lấy những câu chưa được xử lý
            print("\t\t-------START PROCESSS SENTENCE--------")
            result, intent, sub_intent = catch_intent(
                    self,
                    message,
                    conversation_history,
                    conversation_message)

            # ----------------------------- #
            print("\t\t-------Return code-------->",[i for i in result])
            suggest_reply,result,check_end = generate_reply_text(self,result,models.reply_text)

            image = []
            reply_image = suggest_reply
            rep_intent = [key for key in result]
            # 3. Insert data
            tmp = mycol.insert_one({
                'mid' : input_data['mid'],
                'SenderId': input_data['sender_id'],
                'intent': intent,
                'sub_intent': sub_intent,
                'last_conversation': result,
                'message_text': input_data['text'],
                'bot_suggest': suggest_reply,
                'date':time_start
            })
            # ---------------
            returned_res = {'suggest_reply': suggest_reply, 
                    'check_end':check_end, 
                    'rep_intent': rep_intent,
                    'sender_id': input_data['sender_id']
                    }            
                    
            print('RETURNED RES: ', returned_res)
            
        except Exception as e:
            print("IndexError")
            error_type = error_handler(e)
            return {'suggest_reply': "Hệ thống đang gặp vấn đề, bạn vui lòng load lại trang hoặc chờ chút xíu nhenn😭", 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}
        return returned_res
