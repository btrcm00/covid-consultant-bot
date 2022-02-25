from fastapi import FastAPI, Request, File, UploadFile, Form
from backend.config.config import get_config
from backend.process.PretrainedModel import PretrainedModel
from backend.api.api_retrain_model import re_train_model
import pickle
from fastapi.responses import FileResponse
import uvicorn
import logging
import os
import csv
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()

config_app = get_config()

logging.basicConfig(filename=config_app['log']['app'],
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
models = PretrainedModel(config_app['models_chatbot'])
from backend.api.api_message import send_message
from backend.api.api_insert_update_response import insert_update_database


templates =  Jinja2Templates(directory = 'templates')

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

@app.get('/api/update_database_knn')
def update_db():
    data = {
        'question': ['tôi nên sử dụng xà phòng nào để rửa tay'],
        'answer': ['iệc sử dụng xà phòng diệt khuẩn RỬA TAY tốt hơn xà phòng thường trong làm giảm nguy cơ gây bệnh tiêu chảy và nhiễm trùng đường hô hấp.']
    }
    return insert_update_database(data)

@app.get('/api/export_new_data')
def export_data():
    mydb = models.myclient["chatbot_data"]
    mycol = mydb["chatbot_conversations"]
    cursor = mycol.find({})
    data = []
    for doc in cursor:
        if 'intent' in doc:
            intent = doc['intent']
        else:
            intent = ''
        
        if 'sub_intent' in doc:
            sub = doc['sub_intent']
        else:
            sub = ''
        data.append({'text': doc['message_text'], 'intent': intent, 'sub': sub})
    
    with open('data1.csv', encoding='utf8', mode='a+') as csv_file:
        fieldnames = ['text','intent','sub']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        
    return FileResponse(path=os.getcwd() + '/data1.csv', filename='data1.csv', media_type='text/mp4')

@app.get('/api/re_train_model')
def retrain():
    pass
    try:
        re_train_model()
        return 'Done'
    except Exception as e:
        assert type(exception).__name__ == 'NameError'
        assert exception.__class__.__name__ == 'NameError'
        assert exception.__class__.__qualname__ == 'NameError'


@app.post("/data/insert")
async def submit_insert(password: str = Form(...), files: List[UploadFile] = File(...)):
    import pandas as pd
    data = []
    if password != 'congminh':
        return 'SAI MAT KHAU'
    for file in files:
        data = await file.read()
        if not data:
            return 'Vui lòng chọn file data'
        data = pd.read_excel(data)

    return "Đã insert thành công " +  " và ".join([file.filename for file in files])

@app.get('/api/insert_data')
def insert(request: Request):
    return templates.TemplateResponse("insert.html", {"request": request})

# @app.post("/data/update")
# async def submit_update(password: str = Form(...), files: List[UploadFile] = File(...)):
#     import pandas as pd
#     data = []
#     if password != 'congminh':
#         return 'SAI MAT KHAU'
#     for file in files:
#         data = await file.read()
#         data = pd.read_excel(data)

#     return "Đã update thành công " +  " và ".join([file.filename for file in files])

# @app.get('/api/update_data')
# def update_data(request: Request):
#     return templates.TemplateResponse("update.html", {"request": request})



uvicorn.run(app, host=config_app['server']['ip_address'], port=int(config_app['server']['port']))