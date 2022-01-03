import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['NO_PROXY'] = '127.0.0.1'

from datetime import datetime
import sys
sys.path.append("..")

from backend.process.NLU.message_understanding import extract_information_message
from backend.process.DiaglogueManager.dialogue import dialogue
from backend.process.NLG.generate_reply_text import generate_reply_text
from backend.utils.error_handler import error_handler

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

class CovidBot():
    def __init__(self):
        pass
    def reply(self,input_data):
        # get time start
        time_start = datetime.now()
        time_start = time_start.strftime("%Y-%m-%d")
        
        try:
            print("\t\t-------RETRIEVE LAST CONVERSATION FROM DB--------")
            message = input_data['text']
            conversation_history = self.check_mongo(input_data)
            last_infor = {}
            last_intent = ''
            if conversation_history:
                last_intent = list(conversation_history[-1].keys())[0]
                last_infor = conversation_history[-1][last_intent]
            print('Historyyy',conversation_history)

            print("\t\t-------Natural Language Understanding (NLU)--------")
            # Module này để trích xuất các entity và intent từ message của người dùng để sử dụng trong module sau
            # - Intent Classification(IC)
            # - Named Entity Recognition(NER)
            intent, entity_dict = extract_information_message(message)
            print("Output NLU",intent,entity_dict)

            print("\t\t-------Dialogue Manager (DM)--------")
            result = dialogue(message,last_intent,entity_dict, last_infor, intent)
            print("\t\tReturn code->",[i for i in result])

            print("\t\t-------Natural Language Generation (NLG)--------")
            suggest_reply,result,check_end = generate_reply_text(result,models.reply_text,models.response_knn)

            option = []
            rep_intent = [key for key in result]
            if 'choices' in result[rep_intent[0]] and result[rep_intent[0]]['choices'] and len(result[rep_intent[0]]['choices'])>1:
                option = result[rep_intent[0]]['choices']
            print("\t\t-------Insert data to DB--------")
            col = {
                'mid' : input_data['mid'],
                'SenderId': input_data['sender_id'],
                'intent': intent,
                'last_conversation': result,
                'message_text': input_data['text'],
                'bot_suggest': suggest_reply,
                'date':time_start
            }
            print("INSERTMONGGO==>",self.insert_mongo(col))

            # ---------------
            returned_res = {'suggest_reply': suggest_reply, 
                    'check_end':check_end, 
                    'rep_intent': rep_intent,
                    'sender_id': input_data['sender_id'],
                    'option': option
                    }          
                    
            print('RETURNED RES: ', returned_res)
            
        except Exception as e:
            print("IndexError")
            error_type = error_handler(e)
            return {'suggest_reply': "Hệ thống đang gặp vấn đề, bạn vui lòng load lại trang hoặc chờ chút xíu nhenn😭", 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}
        return returned_res
    
    def insert_mongo(self, col):
        try:
            mydb = models.myclient["chatbot_data"]
            mycol = mydb["chatbot_conversations"]
            tmp = mycol.insert_one(col)
        except:
            return False
        return True


    def check_mongo(self, input_data):
        mydb = models.myclient["chatbot_data"]
        mycol = mydb["chatbot_conversations"]
        conversation_history = []
        for ele in mycol.find({'SenderId': input_data['sender_id']}):
            conversation_history.append(ele['last_conversation'])
        
        return conversation_history
