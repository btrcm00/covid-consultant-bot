import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def re_train_knn(Xknn, yknn):
    try:
        knn_tfidf = TfidfVectorizer()
        Xtrain_knn = knn_tfidf.fit_transform(dataknn)
        
        knn = KNeighborsClassifier(n_neighbors=3, metric='cosine')
        knn.fit(Xtrain_knn, yknn)
        
        pickle.dump([dataknn,knn,knntfidf],open('backend/models/knn.pickle','wb'))
        
        return True
    except:
        return False

def re_train_svm(sub_data_sampled):
    Xsub = sub_data_sampled['text'].values
    ysub = list(map(lambda x: map_label(x),sub_data_sampled['sub intent'].values))
    X_train_subsvm, X_test_subsvm, y_train_subsvm, y_test_subsvm = train_test_split(Xsub, ysub, test_size=0.15, random_state=42)
    
    sub_clf = SVC()
    params = {
        'C': np.arange(1,20,1),
        'kernel': ['poly', 'rbf', 'sigmoid'],
    }
    random_subintent_clf = RandomizedSearchCV(sub_clf,param_distributions=params, cv=10, random_state=42)
    random_subintent_clf.fit(Xtrain_subtfidf, y_train_subsvm)
    
    subintent_clf = random_subintent_clf.best_estimator_
    subintent_clf.fit(Xtrain_subtfidf, y_train_subsvm)
    
    pickle.dump([subtfidf, subintent_clf], open('backend/models/sub_svm.pickle','wb'))

def re_train_model():
    pass