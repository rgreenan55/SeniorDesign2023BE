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


#Estimating best parameters for Random Forest
param_grid = [
# Try 12 (3×4) combinations of hyperparameters.
{'n_estimators': [10, 30], 'max_features': [2, 4]},
# Try 6 (2×3) combinations and set bootstrap to False.
{'bootstrap': [False], 'n_estimators': [10, 30], 'max_features':
[3, 4]},
]
rfg = RandomForestRegressor(random_state=42)
# Train across 5 folds, that's a total of (12+6)*5=90 rounds of training.
grid_search = GridSearchCV(rfg, param_grid, cv=5,
scoring='neg_mean_squared_error',
return_train_score=True)
grid_search.fit(x_training_data, y_training_data)
print(grid_search.best_params_)