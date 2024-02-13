import pandas as pd #load CSV files
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt #plots a graph for each feature
from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import pickle

with open('..\\src\\data\\ai_model.pkl', 'rb') as f:
    columns = pickle.load(f)
    model_rf = pickle.load(f)

print("Testing Columns...")
assert columns == ["MedInc", "HouseAge", "AveRooms", "Latitude", "Longitude"], "Test failed!"
print("\tTest passed!")

print("Testing Model...")
assert model_rf.predict([[0, 0, 0, 0, 0]])[0] > 0, "Test failed!"
print("\tTest passed!")