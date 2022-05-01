from tokenize import Number
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import preprocessing

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
from tensorflow.python.keras.backend import dropout
from tensorflow.python.keras.layers.core import Dropout
from imblearn.over_sampling import SMOTE

col_names = ["RSSI_AVG","RSSI_MIN","RSSI_MAX","blckRate","pcktTime","badNode","Node"]
max_depth = 12
Predictors = ["RSSI_AVG","RSSI_MIN","RSSI_MAX"]
target_para = ['Node']

df = pd.read_csv(r'dataSet.csv')



df,target = df.filter(items=Predictors),df.filter(items=target_para)
df= preprocessing.normalize(df)
oversample = SMOTE()
try: 
    df,target = oversample.fit_resample(df, target)
except:
    a = 1
x_train,x_test,y_train,y_test = train_test_split(df,target,random_state = 1,test_size=.3)



clf = tree.DecisionTreeClassifier(max_depth=max_depth)
clf = clf.fit(x_train, np.ravel(y_train))

y_pred = clf.predict(x_test)

# print("MAX depth: ", max_depth)
# print("Predictators: ", Predictors)
# print("Confusion Matrix\n",confusion_matrix(y_true=y_test,y_pred=y_pred))
print("Accuracy decsision tree\n",accuracy_score(y_true=y_test,y_pred=y_pred))




from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(max_depth=max_depth, random_state=0)
clf.fit(x_train, np.ravel(y_train))
y_pred = clf.predict(x_test)

#print("MAX depth: ", max_depth)
#print("Predictators: ", Predictors)
#print("Confusion Matrix\n",confusion_matrix(y_true=y_test,y_pred=y_pred))
print("Accuracy random forest:\n",accuracy_score(y_true=y_test,y_pred=y_pred))



from sklearn import svm
clf = svm.SVC(kernel='rbf') # Linear Kernel
clf.fit(x_train, np.ravel(y_train))
y_pred = clf.predict(x_test)
#print("Confusion Matrix\n",confusion_matrix(y_true=y_test,y_pred=y_pred))
print("Accuracy SVM\n",accuracy_score(y_true=y_test,y_pred=y_pred))


from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(5)
knn.fit(x_train, np.ravel(y_train))
y_pred = knn.predict(x_test)
# print("Confusion Matrix\n",confusion_matrix(y_true=y_test,y_pred=y_pred))
print("Accuracy KNN\n",accuracy_score(y_true=y_test,y_pred=y_pred))









# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Normalization
# from tensorflow.keras import layers

# batch_size = 128
# epochs = 15
# num_nodes = 8

# y_train = keras.utils.to_categorical(y_train)
# y_test = keras.utils.to_categorical(y_test)


# model = keras.Sequential(
#     [
#         keras.Input(shape=len(Predictors)),
#         layers.Dense(50, activation="relu"),
#         layers.Dropout(.4),
#         layers.Dense(150, activation="sigmoid"),
#         layers.Dense(150, activation="relu"),
#         layers.Dense(1, activation="softmax"),
#     ]
# )



# model.compile(loss="mse", optimizer="sgd", metrics=["CategoricalAccuracy"])

# model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

# score = model.evaluate(x_test, y_test, verbose=0)
# print("Test loss:", score[0])
# print("Test accuracy:", score[1])

