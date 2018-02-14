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
from sklearn.pipeline import make_pipeline
from sklearn import svm
from featureExtraction import *


def evaluationMetrics(X,Y):

    beat = False
    
    for clf, name in (
            (KNeighborsClassifier(n_neighbors=1,n_jobs=8), "k-Nearest Neighbor"),
            (linear_model.LogisticRegression(C=0.5),"Logistic Regression"),
            (RandomForestClassifier(max_depth=50, n_estimators=100, max_features=25,n_jobs=8), "Random forest")):
            #(svm.SVC(kernel='linear',probability = True), "linear-SVM"),
            #(svm.SVC(kernel='rbf',probability = True), "rbf-SVM")):
        print('=' * 80)
        print(name)
        classifier = execution(clf,X,Y)
        if(not beat and name == "Random forest"):
            beat = True
            beatTheBenchmark(classifier,"test_set.csv")

def execution(classifier,X,Y):

    # vectorizer=CountVectorizer()
    # transformer=TfidfTransformer()
    # svd=TruncatedSVD(n_components=20, random_state=42)
    #
    # pipeline = Pipeline([
    #     # ('vect', vectorizer),
    #     # ('tfidf', transformer),
    #     ('svd',svd),
    #     ('clf', classifier)
    # ])
    # #tuned_parameters={'svd__n_components':[10,20,30,50],'tfidf__use_idf':(True,False)}
    # clf = make_pipeline(pipeline)

    scores = cross_val_score(classifier, X, Y, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    classifier.fit(X,Y)
    return classifier

def beatTheBenchmark(classifier,filename):

    df = pd.read_csv(filename,sep=';')
    X,Y = getGridRepresentation(df.values.tolist())

    predicted = classifier.predict(X)

    p = pd.DataFrame({'Test_Trip_ID':Y,'Predicted_JourneyPatternID':predicted})
    p.to_csv('testSet_JourneyPatternIDs.csv', sep='\t', encoding='utf-8',
    index=False,header=True,columns=['Test_Trip_ID','Predicted_JourneyPatternID'])
