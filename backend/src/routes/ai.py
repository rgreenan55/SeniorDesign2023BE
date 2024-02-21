from routes import app
from flask import request
import random
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
import time

with open('data\\ottawa_ai_model.pkl', 'rb') as f:
    columns = pickle.load(f)
    model_rf = pickle.load(f)

@app.route('/')
def home():
    return '''<a href="/get-house-price-by-address?address=615 Reid St, Fredericton, NB, CA">Get Price By Address</a><br><br>
    <a href="/get-ai-url">Get AI Test URL</a>  -  <a href="/get-ai-args">Get AI Args</a><br><br>
    <br><br>
    <a href="/get-house-price-by-address-test?address=615 Reid St, Fredericton, NB, CA">Get Test Price By Address</a><br><br>
    <a href="/get-test-url">Get Test URL</a>  -  <a href="/get-ai-args-test">Get Test AI Args</a><br><br>
    '''

# @app.route('/get-house-info')
# def get_house_info():
#     if not 'address' in request.args:
#         return "No address provided, use the format /get-house-info?address='address'"
#     address = request.args.get('address')
#     if address == None or address == "":
#         return "No address provided"
#     if address in house_info_list_test:
#         house_info = house_info_list_test[address]
#     else:
#         house_info = "Balls" 
#     return house_info

def populateHouseInfoListTest(house_info_list_test):
    house_info_list_test["615 Reid St, Fredericton, NB, CA"] = {'bedrooms': 5, 'bathrooms': 2, 'sqft_living': 1500, 'sqft_lot': 10000, 'floors': 1, 'yr_built': 1990, 'yr_renovated': 2010, 'postal_code': 52345, 'lat': 45.9516307, 'long': -66.6493478}
    house_info_list_test["test"] = house_info_list_test["615 Reid St, Fredericton, NB, CA"]

def populateHouseInfoList(house_info_list):
    with open('data\\ottawa_eval_data.pkl', 'rb') as f:
        x_test_data = pickle.load(f)
        y_test_data = pickle.load(f).tolist()
        for i in range(len(x_test_data)):
            info = {"data" : x_test_data[i], "price" : y_test_data[i]}
            house_info_list.append(info)

def getArgsByAddress(address):
    if address == None or address == "":
        return {"status": False, "data": "No address provided"}
    if address in house_info_list:
        return {"status": True, "data": house_info_list[address]}
    else:
        return {"status": False, "data": "House Not Available"}
    
def getArgsByAddressTest(address):
    print(address)
    if address == None or address == "":
        return {"status": False, "data": "No address provided"}
    if address in house_info_list_test:
        return {"status": True, "data": house_info_list_test[address]}
    else:
        return {"status": False, "data": "House Not Available"}

@app.route('/get-house-price')
def get_house_price():
    argsList = get_ai_args()
    queryArgs = {}
    if "price" in request.args:
        price = int(float(request.args.get("price")))
    else:
        price = 0
    for arg in argsList:
        if arg in request.args:
            queryArgs[arg] = request.args.get(arg)
        else:
            queryArgs[arg] = 0
    value = queryAI(queryArgs)
    print(value, price)
    return {"estimate" : value, "actual" : price, "difference" : value - price, "percent" : (value - price) / (price+0.000001) * 100}

@app.route('/get-house-price-by-address')
def get_house_price_address():
    if not 'address' in request.args:
         return "No address provided"
    queryArgs = getArgsByAddress(request.args.get("address"))
    if not queryArgs["status"]:
        return queryArgs["data"]
    value = queryAI(queryArgs["data"])
    return {"estimate" : value, "actual" : 0}

@app.route('/get-house-price-test')
def get_house_price_test():
    argsList = get_ai_args_test()
    queryArgs = {}
    for arg in argsList:
        if arg in request.args:
            queryArgs[arg] = request.args.get(arg)
        else:
            queryArgs[arg] = 0
    value = queryAITest(queryArgs)
    return {"estimate" : value, "actual" : 0}

@app.route('/get-house-price-by-address-test')
def get_house_price_address_test():
    if not 'address' in request.args:
         return "No address provided"
    queryArgs = getArgsByAddressTest(request.args.get("address"))
    if not queryArgs["status"]:
        return queryArgs["data"]
    value = queryAITest(queryArgs["data"])
    return {"estimate" : value, "actual" : 0}
    

@app.route('/get-ai-args')
def get_ai_args():
    print(columns)
    return columns

@app.route('/get-ai-args-test')
def get_ai_args_test():
    return ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "yr_built", "yr_renovated", "postal_code", "lat", "long"]

def queryAI(query):
    query = pd.DataFrame(query, index=[0])
    value = model_rf.predict(query)[0]
    return value

def queryAITest(query):
    value = 0
    value += int(query["bedrooms"]) * 1000
    value += int(query["bathrooms"]) * 1000
    value += int(query["sqft_living"]) * 100
    value += int(query["sqft_lot"]) * 25
    value += int(query["floors"]) * 1000
    value += ((int(query["yr_built"]) - 1950) * 100) if int(query["yr_built"]) != 0 else 0
    value += ((int(query["yr_renovated"]) - 2010) * 1000) if int(query["yr_renovated"]) != 0 else 0
    value += int(query["postal_code"]) * 1
    return value

@app.route('/get-test-url')
def get_test_url():
    params = {}
    params["bedrooms"] = random.randint(1, 5)
    params["bathrooms"] = max(params["bedrooms"] + random.randint(-2, 1), 1)
    params["sqft_living"] = random.randint(500, 5000)
    params["sqft_lot"] = params["sqft_living"] + random.randint(500, 5000)
    params["floors"] = random.randint(1, 3)
    params["yr_built"] = random.randint(1900, 2023)
    params["yr_renovated"] = random.randint(params["yr_built"], 2024)
    params["postal_code"] = random.randint(48000, 98100)
    params["lat"] = random.randint(47, 48)
    params["long"] = random.randint(-122, -121)
    url = "http://localhost:5000/get-house-price-test?"
    for param in params:
        url += param + "=" + str(params[param]) + "&"
    return "<a href=" + url[:-1] + ">" + url[:-1] + "</a>"

@app.route('/get-ai-url')
def get_ai_url():
    params = {}
    test_data = house_info_list[random.randint(0, len(house_info_list) - 1)]
    columns = get_ai_args()
    for i in range(len(columns)):
        params[columns[i]] = test_data["data"][i]
    print(test_data)
    url = "http://localhost:5000/get-house-price?"
    for param in params:
        url += param + "=" + str(params[param]) + "&"
    url += "price=" + str(test_data["price"])
    return "<a href=" + url + ">" + url + "</a>"

@app.route('/test-throughput')
def test_throughput():
    if not 'count' in request.args:
        return "No count provided"
    try:
        testCount = int(request.args.get("count"))
    except:
        return "Invalid count"
    startTime = time.time()
    for i in range(testCount):
        params = {}
        test_data = house_info_list[random.randint(0, len(house_info_list) - 1)]
        columns = get_ai_args()
        for i in range(len(columns)):
            params[columns[i]] = test_data["data"][i]
        queryAI(params)
    timeTaken = time.time() - startTime
    return {"time" : timeTaken, "timePerQuery" : timeTaken / testCount}

house_info_list_test = {}
populateHouseInfoListTest(house_info_list_test)
house_info_list = []
populateHouseInfoList(house_info_list)
