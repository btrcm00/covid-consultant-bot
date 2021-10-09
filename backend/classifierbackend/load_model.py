from keras.models import load_model
import os
import json
import pickle

#intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']
path = os.getcwd()

#LSTM
model_lstm =load_model(path + '/model/lstm')
token_lstm = pickle.load(open(path + '/model/lstm/tokenizer.pickle','rb'))
label_lstm = pickle.load(open(path + '/model/lstm/label.pickle','rb'))

#SVM
tfidf_svm, model_svm = pickle.load(open('./model/svm.pickle', 'rb'))