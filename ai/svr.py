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

#print(houses["HouseAge"].value_counts())

#checks if certain features have null values
print(houses.isna().sum())

#Visualizes the data to see the feature distributions and which ones have extreme disparities/values, which in this case is average bedrooms, rooms, populations and occupation
houses.hist(figsize=(12, 10), bins=30, edgecolor="black")
plt.subplots_adjust(hspace=0.7, wspace=0.4)
#plt.show()

sns.scatterplot(
    data=california_housing.frame,
    x="Longitude",
    y="Latitude",
    size="MedHouseVal",
    hue="MedHouseVal",
    palette="viridis",
    alpha=0.5,
)

#plots the scatterplot to show the relationship between median house value and the longitude and latitude of a house. 
plt.legend(title="MedHouseVal", bbox_to_anchor=(1.05, 0.95), loc="upper left")
_ = plt.title("Median house value depending of\n their spatial location")
#plt.show()

#show correlations of each feature to target variable (in this case MedHouseVal)
corr_matrix = houses.corr()
corr_matrix["MedHouseVal"].sort_values(ascending=False)
print(corr_matrix)

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

model_svr = SVR(kernel="rbf",C=50, gamma="auto",epsilon=0.5)
model_svr.fit(x_training_data,y_training_data)
predictions_svr = model_svr.predict(x_test_data)
lin_mse = mean_squared_error(y_test_data, predictions_svr)
lin_rmse = np.sqrt(lin_mse)
print(lin_rmse * 100000)
