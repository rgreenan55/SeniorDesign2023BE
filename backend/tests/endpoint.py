import requests
import json

print("Testing Endpoints...")
print("\tTesting '/get-house-price-by-address' route...")
print("\t\tTesting valid address...")
print("\t\t\tTest skipped!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# response = requests.get('http://localhost:5000/get-house-price-by-address?address=615 Reid St, Fredericton, NB, CA')
#assert json.loads(response.text) == {"estimate": 464345, "actual": 0}, "Test failed!"
# assert json.loads(response.text)["estimate"] > 100000, "Test failed!"
# print("\t\t\tTest passed!")
print("\t\tTesting invalid address...")
response = requests.get('http://localhost:5000/get-house-price-by-address?address=0 Trash St, Alimor, WA, BG')
assert response.text == "House Not Available", "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting missing address...")
response = requests.get('http://localhost:5000/get-house-price-by-address')
assert response.text == "No address provided", "Test failed!"
print("\t\t\tTest passed!")

print("\tTesting '/get-house-price' route...")
print("\t\tTesting valid request...")
response = requests.get('http://localhost:5000/get-house-price?latitude=-0.31813540868566553&longitude=-0.12202669588731199&yearBuilt=-1.4130506410288362&bedrooms=-0.04998328502943571&bathrooms=-1.4194580327441408&garage=-0.11047644433014096&lotDepth=0.2782542693996436&lotFrontage=-0.050373727047793235&postalCode=0.5188980370188913&propertyType=0.17158819513824788&style=0.01329895128605074&price=749900.0')
assert json.loads(response.text)["estimate"] > 1, "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting missing arguments...")
response = requests.get('http://localhost:5000/get-house-price')
assert json.loads(response.text)["estimate"] > 0, "Test failed!"
print("\t\t\tTest passed!")

print("\tTesting '/get-ai-args' route...")
response = requests.get('http://localhost:5000/get-ai-args')
assert json.loads(response.text) == ['yearBuilt', 'bedrooms', 'bathrooms', 'parking', 'garage', 'lotDepth', 'lotFrontage', 'postalCode', 'propertyType', 'style'], "Test failed!"
print("\t\tTest passed!")

print("\tTesting AI Speed...")
print("\t\tSingle query...")
response = requests.get("http://localhost:5000/test-throughput?count=1")
assert json.loads(response.text)["timePerQuery"] < 0.005, "Test failed!"
print("\t\t\tTest passed!")
print("\t\t10 queries...")
response = requests.get("http://localhost:5000/test-throughput?count=10")
assert json.loads(response.text)["timePerQuery"] < 0.005, "Test failed!"
print("\t\t\tTest passed!")
print("\t\t100 queries...")
response = requests.get("http://localhost:5000/test-throughput?count=100")
assert json.loads(response.text)["timePerQuery"] < 0.005, "Test failed!"
print("\t\t\tTest passed!")