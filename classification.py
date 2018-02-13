from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from pandas import *
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from scipy import spatial
from sklearn.metrics  import *
import string
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import linear_model


def evaluationMetrics(X,Y):

    for clf, name in (
            (KNeighborsClassifier(n_neighbors=3,n_jobs=-1), "k-Nearest Neighbor"),
            # (svm.SVC(kernel='linear',probability = True), "SVM"),
            # (linear_model.LogisticRegression(C=1e5),"Logistic Regression"),
            (RandomForestClassifier(max_depth=25, n_estimators=10, max_features=5), "Random forest")):
        print('=' * 80)
        print(name)
        execution(clf,X,Y)



def execution(classifier,X,Y):

    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    svd=TruncatedSVD(n_components=20, random_state=42)

    pipeline = Pipeline([
        ('vect', vectorizer),
        ('tfidf', transformer),
        ('svd',svd),
        ('clf', classifier)
    ])
    #tuned_parameters={'svd__n_components':[10,20,30,50],'tfidf__use_idf':(True,False)}
    clf = GridSearchCV(pipeline, {}, cv=10,n_jobs=-1)

    scores = cross_val_score(classifier, X, Y, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    # clf.fit(X_train,Y_train_true).predict_proba(X_test)
    # predicted=clf.predict(X_test)
    # print accuracy_score(Y_test_true, predicted)
