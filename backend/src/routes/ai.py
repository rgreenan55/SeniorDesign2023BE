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
    normalizer = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '''<a href="/get-assessment-by-address?address=1466 Launay Avenue, Ottawa, Ontario">Get Price By Address</a><br><br>
    <a href="/get-ai-url">Get AI Test URL</a>  -  <a href="/get-ai-args">Get AI Args</a><br><br>
    <a href="/get-all-addresses">Get All Addresses</a> - <a href="/get-all-addresses-by-prefix?prefix=1466">Get Addresses By Prefix</a><br><br>
    <a href="/get-random-address-and-attributes">Get Random Address and Attributes</a><br><br>
    <a href="/get-random-address-and-attributes-with-results">Get Random Address and Attributes with Results</a><br><br>
    <a href="/get-AI-accuracy">Get AI Accuracy</a><br><br>
    <a href="/test-throughput?count=100">Test Throughput</a><br><br>
'''

def populateHouseInfoList(house_info_list):
    with open('data\\ottawa_eval_data.pkl', 'rb') as f:
        x_test_data = pickle.load(f)
        y_test_data = pickle.load(f).tolist()
        for i in range(len(x_test_data)):
            info = {"data" : x_test_data[i], "price" : y_test_data[i]}
            house_info_list.append(info)
    return house_info_list

def populateHouseInfoObject():
    with open('data\\ottawa_eval_data_with_addr_formatted.pkl', 'rb') as f:
        houses = pickle.load(f)
    return houses

def getArgsByAddress(address):
    if address == None or address == "":
        return {"status": False, "data": "No address provided"}
    if address in house_info_list:
        return {"status": True, "data": house_info_list[address]}
    else:
        return {"status": False, "data": "House Not Available"}

@app.route('/get-assessment-by-arguments')
def get_house_price():
    argsList = get_ai_args()
    queryArgs = {}
    if "price" in request.args:
        price = float(request.args.get("price"))
    else:
        price = 0
    for argDict in argsList:
        arg = argDict["name"]
        if arg in request.args:
            queryArgs[arg] = request.args.get(arg)
        else:
            queryArgs[arg] = 0
    value = queryAI(queryArgs)
    # value *= 100000
    # price *= 100000
    # print(value, price)
    return {"estimate" : value, "actual" : price, "difference" : value - price, "percent" : (value - price) / (price+0.000001) * 100}

@app.route('/get-assessment-by-address')
def get_house_price_address():
    if not 'address' in request.args:
         return {"error" : "true" , "reason" : "No address provided"}
    queryArgs = getArgsByAddress(request.args.get("address"))
    if not queryArgs["status"]:
        return {"error" : "true" , "reason" : queryArgs["data"]}
    argsList = get_ai_args()
    query = {}
    queryData = normalizer.inverse_transform([queryArgs["data"]["data"]])[0]
    for i in range(len(argsList)):
        query[argsList[i]["name"]] = queryData[i]
    print(query)
    value = queryAI(query)
    actual = queryArgs["data"]["price"]
    return {"estimate" : value, "actual" : actual, "difference" : value - actual, "percent" : (value - actual) / (actual+0.000001) * 100, "lat" : query["latitude"], "lng" : query["longitude"]}

@app.route('/get-all-addresses-by-prefix')
def search_for_address_prefix():
    if not 'prefix' in request.args:
        return {"error" : "No prefix provided"}
    prefix = request.args.get('prefix')
    addresses = get_all_addresses()
    matches = []
    for address in addresses:
        if address["address"].startswith(prefix):
            matches.append(address)
    return matches

@app.route('/get-all-addresses')
def get_all_addresses():
    output = []
    for house in house_info_list.keys():
        output.append({"address" : house, "lat" : house_info_list[house]["address"]["lat"], "lng" : house_info_list[house]["address"]["lon"]})
    return output

@app.route('/get-random-address-and-attributes')
def get_random_address_and_attributes():
    address = random.choice(list(house_info_list.keys()))
    data = normalizer.inverse_transform([house_info_list[address]["data"]])[0]
    columns = get_ai_args()
    args = {}
    for i in range(len(columns)):
        args[columns[i]["name"]] = data[i]
    return {"address" : address, "lat" : house_info_list[address]["address"]["lat"], "lng" : house_info_list[address]["address"]["lon"], "attributesObj" : args, "attributesList" : list(data)}

@app.route('/get-AI-accuracy')
def get_ai_accuracy():
    percentageDifference = 0
    for address in house_info_list.keys():
        params = {}
        data = house_info_list[address]
        test_data = {"data" : normalizer.inverse_transform([data["data"]])[0], "price" : data["price"]}
        columns = get_ai_args()
        for i in range(len(columns)):
            params[columns[i]["name"]] = test_data["data"][i]
        estimate = queryAI(params)
        percentageDifference += abs(estimate - house_info_list[address]["price"]) / (house_info_list[address]["price"] + 0.000001) * 100
    return {"precentDiff" : percentageDifference / len(house_info_list), "accuracy" : 100 - percentageDifference / len(house_info_list)}

@app.route('/get-random-address-and-attributes-with-results')
def get_random_address_and_attributes_with_results():
    house = get_random_address_and_attributes()
    price = house_info_list[house["address"]]["price"]
    estimate = queryAI(house["attributesObj"])
    return {"house" : house, "results" : {"price" : price, "estimate" : estimate, "difference" : estimate - price, "percent" : (estimate - price) / (price+0.000001) * 100}}

@app.route('/get-ai-args')
def get_ai_args():
    return columns

def queryAI(query):
    # print("Query: \n", query, "\n")
    query = pd.DataFrame(query, index=[0])
    # print("Before Normalized: \n", query, "\n")
    query = normalizer.transform(query)
    # print("After Normalized: \n", query, "\n")
    value = model_rf.predict(query)[0]
    return value

@app.route('/get-ai-url')
def get_ai_url():
    params = {}
    data = house_info_list[list(house_info_list.keys())[random.randint(0, len(house_info_list) - 1)]]
    # print(test_data)
    test_data = {"data" : normalizer.inverse_transform([data["data"]])[0], "price" : data["price"]}
    # print(test_data)
    columns = get_ai_args()
    for i in range(len(columns)):
        params[columns[i]["name"]] = test_data["data"][i]
    #print(test_data)
    url = "http://localhost:5000/get-assessment-by-arguments?"
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
        data = house_info_list[list(house_info_list.keys())[random.randint(0, len(house_info_list) - 1)]]
        test_data = {"data" : normalizer.inverse_transform([data["data"]])[0], "price" : data["price"]}
        columns = get_ai_args()
        for i in range(len(columns)):
            params[columns[i]["name"]] = test_data["data"][i]
        queryAI(params)
    timeTaken = time.time() - startTime
    return {"time" : timeTaken, "timePerQuery" : timeTaken / testCount}

house_info_list = populateHouseInfoObject()
