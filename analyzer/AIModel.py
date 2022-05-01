from itertools import tee
from tokenize import Number
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse.sputils import matrix 
from sklearn import tree
from sklearn import preprocessing
from sklearn.preprocessing import label_binarize

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.metrics import plot_confusion_matrix
# from tensorflow.python.keras.backend import dropout
# from tensorflow.python.keras.layers.core import Dropout







from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

def AITrain(Predictors):
    """col_names = ["RSSI_AVG","RSSI_MIN","RSSI_MAX","RSSI_range","RSSI_STD","blckRate","pcktTime","badNode","Node"]"""
    max_depth = 16

    df = pd.read_csv(r'dataSet.csv')
    
    target_para = ['Node']





    df,target = df.filter(items=Predictors),df.filter(items=target_para)
    df= preprocessing.normalize(df)
    oversample = SMOTE()
    try: 
        df,target = oversample.fit_resample(df, target)
    except:
        a = 1


    x_train,x_test,y_train,y_test = train_test_split(df,np.ravel(target),random_state = 1,test_size=.7)



    clf = RandomForestClassifier(max_depth=max_depth, random_state=0)
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

    target  = nodes_toBadGoodNodes(target)
    scores = cross_val_score(clf, df, np.ravel(target), scoring='roc_auc', cv=cv, n_jobs=-1)
    
    clf.fit(x_train, np.ravel(y_train))
    y_pred = clf.predict(x_test)


    print("Predictors\n",Predictors)
    print("Confusion Matrix\n",confusion_matrix(y_true=y_test,y_pred=y_pred))
    print("Accuracy\n",accuracy_score(y_true=y_test,y_pred=y_pred))

    plot_confusion_matrix(clf, x_test, y_test)
    plt.savefig("/home/moh/Documents/PhD/research/analyzer/img/conf/mat"+str(accuracy_score(y_true=y_test,y_pred=y_pred))+".png")
    plt.close()
    
    y_pred = nodes_toBadGoodNodes(y_pred)
    y_test = nodes_toBadGoodNodes(y_test)

    confMat = confusion_matrix(y_true=y_test,y_pred=y_pred)
    print("Confusion Matrix\n",confMat)
    acu = accuracy_score(y_true=y_test,y_pred=y_pred)
    print("Accuracy\n",acu)



    # plt.show()


    from sklearn.metrics import f1_score
    f_score = f1_score(y_true=y_test,y_pred=y_pred)
    auc  = round(sum(scores)/len(scores),4)
    print("F1-score\n",f_score)
    print("AUC Score\n"+ str(auc))

    return acu,f_score,auc, confMat[1][0]/(confMat[1][0]+confMat[1][1]),confMat, clf


def nodes_toBadGoodNodes(x):
    try:
        label = x.to_numpy().copy()
    except:
        label= x

    for i in range(len(label)):
        if label[i] == 7:
            label[i] = 1
        else:
            label[i] = 0
    return label

