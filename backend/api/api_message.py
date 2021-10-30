import pickle
import sys
import json
sys.path.append('.')
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()
from backend.config.config import get_config
config_app = get_config()
from backend.process.create_chatbot.chatbot import CovidBot

def send_message(data):
# ---------------- 4.BOT ---------------- #
    print("\t\t+++++++++++++++ Start API send-message +++++++++++++++\n\n")

    ls_param = ['sender_id', 'recipient_id', 'mid', 'text']
    # -------------------- Check and add missing params of request -------------------- #
    print("\t\t+++++++++++++++ Check and add missing params of request +++++++++++++++")
    for ele in ls_param:
        if ele not in data or not data[ele]:
            # THROW ERROR because of not enough param
            return {'suggest_reply': 'ERROR NOT ENOUGH PARAM', 'id_job': '', 'check_end': True}

    # Add values to each of params - Dictionary
    input_data = {ele: data[ele] for ele in ls_param}
    data = input_data

    print("\t\t+++++++++++ 3.BOT +++++++++++")
    chatbot = CovidBot()
    result = chatbot.reply(data)
    # ------------------------------------------- #
    
    return result