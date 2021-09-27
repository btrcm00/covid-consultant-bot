from django.http import JsonResponse
import pickle
import json
import pandas as pd
import numpy as np
from .models import Conversation, Client, Infor
from .text_process import text_preprocess


symptoms = []
def response(request):
    data = json.loads(request.body)
    text = text_preprocess(data['text'])
    symptoms.append(text)
    print(symptoms)
    return JsonResponse({'label':'hihi'})

def conversation(request):
    data = json.loads(request.body)
    conv = data['conversation'].encode().decode('utf-8')
    nums = Conversation.objects.count() + 1
    conversation = Conversation.objects.create(content=conv,num=nums)
    return JsonResponse({'conv': conv})