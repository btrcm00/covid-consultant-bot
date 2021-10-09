from django.http import JsonResponse
import pickle
import json
import pandas as pd
import numpy as np
from .models import Conversation, Client, Infor
from .text_process import text_preprocess
import pickle
import json

#intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']

with open('D:\\211\\decuongluanvan\\backend\\classifierbackend\\reply.json', encoding='utf-8') as f:
    reply = json.load(f)
tfidf_intent, model_intent = pickle.load(open('./model/svm.pickle', 'rb'))

symptoms = []
def response(request):
    data = json.loads(request.body)
    text = text_preprocess(data['text'])

    intent = model_intent.predict(tfidf_intent.transform([text]))[0]
    
    symptoms.append(text)
    return JsonResponse({'label':reply[intent]})

def conversation(request):
    data = json.loads(request.body)
    conv = data['conversation'].encode().decode('utf-8')
    nums = Conversation.objects.count() + 1
    conversation = Conversation.objects.create(content=conv,num=nums)
    return JsonResponse({'conv': conv})