import os
import json
import pickle

#intent: ['current_numbers''symptom''covid_infor''Hello''OK''Other''how_spreading''precautions''medication''emergency_contact']
path = os.getcwd()

#SVM
tfidf_svm, model_svm = pickle.load(open('./model/svm.pickle', 'rb'))
tfidf_intent, model_intent = pickle.load(open('./model/intent_svm.pickle', 'rb'))