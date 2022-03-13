import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from backend.config.config import get_config
config_app = get_config()
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel(config_app['models_chatbot'])
mydb = models.myclient["chatbot_data"]
mycol = mydb["data_intent"]

def re_train_knn(Xknn, yknn):
    # try:
    knn_tfidf = TfidfVectorizer()
    Xtrain_knn = knn_tfidf.fit_transform(Xknn)
    
    knn_model = KNeighborsClassifier(n_neighbors=3, metric='cosine')
    knn_model.fit(Xtrain_knn, yknn)
    
    print("train score knn",knn_model.score(Xtrain_knn, yknn))
    
    pickle.dump([Xknn,knn_model,knn_tfidf],open('./models/knn_new.pickle','wb'))
    print('done')
    return True
    # except:
    #     return False

def re_train_svm(X, y):
    # Xsub = sub_data_sampled['text']
    # ysub = list(map(lambda x: map_label(x),sub_data_sampled['sub intent'].values))
    X_train_subsvm, X_test_subsvm, y_train_subsvm, y_test_subsvm = train_test_split(X, y, test_size=0.1, random_state=42)
    
    subtfidf = TfidfVectorizer()

    Xtrain_subtfidf = subtfidf.fit_transform(X_train_subsvm)
    
    sub_clf = SVC()
    params = {
        'C': np.arange(1,20,1),
        'kernel': ['poly', 'rbf', 'sigmoid'],
    }
    random_subintent_clf = RandomizedSearchCV(sub_clf,param_distributions=params, cv=10, random_state=42)
    random_subintent_clf.fit(Xtrain_subtfidf, y_train_subsvm)
    
    subintent_clf = random_subintent_clf.best_estimator_
    subintent_clf.fit(Xtrain_subtfidf, y_train_subsvm)
    
    print("train score svm",subintent_clf.score(Xtrain_subtfidf, y_train_subsvm))
    print("test score svm",subintent_clf.score(subtfidf.transform(X_test_subsvm), y_test_subsvm))
    
    pickle.dump([subtfidf, subintent_clf], open('./models/sub_svm_new.pickle','wb'))

def re_train_model():
    Xknn=[]
    yknn=[]    
    cursor = mycol.find({})
    for doc in cursor:
        if doc['intent'].lower()!='request' or type(doc['text']) != str:
            continue
        
        Xknn.append(doc['text'])
        yknn.append(doc['sub_intent'])
    
    re_train_knn(Xknn,yknn)
    print('Retrain knn done!')
    re_train_svm(Xknn,yknn)
    print('Retrain svm done!')
    return 'Done'