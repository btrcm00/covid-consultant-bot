
from fastapi import FastAPI, Request
from backend.config.config import get_config
from backend.process.PretrainedModel import PretrainedModel
import pickle
import uvicorn
import logging
from fastapi.encoders import jsonable_encoder
app = FastAPI()

config_app = get_config()

logging.basicConfig(filename=config_app['log']['app'],
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
models = PretrainedModel(config_app['models_chatbot'])
from backend.api.api_message import send_message

@app.post('/api/send-message')
async def api_send_message(request: Request):
    json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    result = send_message(json_param)
    return result
@app.post('/api/send-image')
async def api_send_image(request: Request):
    ''' json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    result = send_image(json_param) '''
    result = {
        'rep_intent': 'inform',
        'suggest_reply': 'Hiện tại chatbot chưa hỗ trợ tính năng gửi ảnh, tính năng này sẽ có trong thời gian sớm nhất ạ.',
        'id_job': 456363,
        'check_end':False
    }
    return result

@app.get('/')
def home():
    mydb = models.myclient["chatbot_data"]
    mycol = mydb["chatbot_conversations"]
    return "Covid-chatbot " + str(mycol.count_documents({}))

uvicorn.run(app, host=config_app['server']['ip_address'], port=int(config_app['server']['port']))