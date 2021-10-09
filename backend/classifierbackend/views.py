from django.http import JsonResponse
import pickle
import json
import pandas as pd
import numpy as np
import os
from keras.preprocessing.sequence import pad_sequences
from .load_model import model_lstm, token_lstm, label_lstm, tfidf_svm, model_svm
from .models import Conversation, Client, Infor
from .text_process import text_preprocess
#intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']
path = os.getcwd()
with open(path + '\\classifierbackend\\reply.json', encoding='utf-8') as f:
    reply = json.load(f)

symptoms = []
def response(request):
    data = json.loads(request.body)
    text = text_preprocess(data['text'])
    print(text)
    
    #svm
    intent_svm = model_svm.predict(tfidf_svm.transform([text]))[0]
    vote_svm = model_svm.decision_function(tfidf_svm.transform([text]))
    prob_svm = np.exp(vote_svm)/np.sum(np.exp(vote_svm),axis=1, keepdims=True)
    #lstm
    prob_lstm = model_lstm.predict(pad_sequences(token_lstm.texts_to_sequences([text]),maxlen=len(token_lstm.word_counts)+1))
    intent_lstm = label_lstm[np.argmax(prob_lstm)]
    print("SVM: {}-{}\nLSTM: {}-{}".format(intent_svm, np.max(prob_svm), intent_lstm, np.max(prob_lstm)))
    intent = intent_svm if np.max(prob_svm) > np.max(prob_lstm) else intent_lstm

    symptoms.append(text)
    
    return JsonResponse({'label':reply[intent]})

def conversation(request):
    data = json.loads(request.body)
    conv = data['conversation'].encode().decode('utf-8')
    nums = Conversation.objects.count() + 1
    conversation = Conversation.objects.create(content=conv,num=nums)
    return JsonResponse({'conv': conv})