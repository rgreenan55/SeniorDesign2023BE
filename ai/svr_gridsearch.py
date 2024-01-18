import pandas as pd #load CSV files
from sklearn.datasets import fetch_california_housing #dummy dataset for california housing
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt #plots a graph for each feature
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV


#Dummy data
california_housing = fetch_california_housing(as_frame=True)

#Prints info of dummy data
california_housing.frame.info()

#data fram containing dummy data
houses = california_housing.frame

#drop columns based on what was concluded from the visualizations (is there a way to make this automatic???)
cols = ['AveBedrms', 'Population', 'AveOccup']
houses = houses.drop(columns = cols, axis = 1)

#Split original dataset
x_data = houses.drop('MedHouseVal', axis = 1)
y_data = houses['MedHouseVal']

#20% of original data set is used as test data
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x_data, y_data, test_size = 0.20, random_state=2)

#Normalizes the data to a clean graph
sc = StandardScaler()
x_training_data = sc.fit_transform(x_training_data)
x_test_data = sc.fit_transform(x_test_data)


#Grid search to find best parameters for SVR
param = {"kernel" : ("rbf", "poly"), "C": [10,50,100], "gamma": ["scale", "auto", 1e-7], "epsilon": [0.1,0.2,0.5]}
test_svr = SVR()
clf = GridSearchCV(test_svr,param)
clf.fit(x_training_data, y_training_data)
print(clf.best_params_)
#best was {'C': 50, 'epsilon': 0.5, 'gamma': 'auto', 'kernel': 'rbf'}