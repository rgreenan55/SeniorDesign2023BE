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
import pickle

#load dataset
with open('ai_model.pkl', 'rb') as f:
    columns = pickle.load(f)
    model_rf = pickle.load(f)
with open('eval_data.pkl', 'rb') as f:
    x_test_data = pickle.load(f)
    y_test_data = pickle.load(f)

predictions_rf = model_rf.predict(x_test_data)
lin_mse = mean_squared_error(y_test_data, predictions_rf)
lin_rmse = np.sqrt(lin_mse)
print("Columns used in model: ", columns)
print(lin_rmse * 100000) #100 000 because median house value needs to be represented in one hundreds of thousands (i.e. the value 1 is $100 000)