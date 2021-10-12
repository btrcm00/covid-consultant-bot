from django.http import JsonResponse
import json
from .models import Conversation, Client, Infor
from .text_process import text_preprocess
from .reply import reply


symptoms = []
def response(request):
    data = json.loads(request.body)
    text = text_preprocess(data['text'])
    print(text)
    response = reply(text)

    symptoms.append(response)
    
    return JsonResponse({'label':response})
 
def conversation(request):
    data = json.loads(request.body)
    conv = data['conversation'].encode().decode('utf-8')
    nums = Conversation.objects.count() + 1
    conversation = Conversation.objects.create(content=conv,num=nums)
    return JsonResponse({'conv': conv})