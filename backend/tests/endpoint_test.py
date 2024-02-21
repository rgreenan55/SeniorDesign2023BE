import requests
import json

print("Testing Endpoints...")
print("\tTesting '/get-house-price-by-address-test' route...")
print("\t\tTesting valid address...")
response = requests.get('http://localhost:5000/get-house-price-by-address-test?address=615 Reid St, Fredericton, NB, CA')
assert json.loads(response.text) == {"estimate": 464345, "actual": 0}, "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting invalid address...")
response = requests.get('http://localhost:5000/get-house-price-by-address-test?address=0 Trash St, Alimor, WA, BG')
assert response.text == "House Not Available", "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting missing address...")
response = requests.get('http://localhost:5000/get-house-price-by-address-test')
assert response.text == "No address provided", "Test failed!"
print("\t\t\tTest passed!")

print("\tTesting '/get-house-price' route...")
print("\t\tTesting valid request...")
response = requests.get('http://localhost:5000/get-house-price-test?bedrooms=5&bathrooms=2&sqft_living=1500&sqft_lot=10000&floors=1&yr_built=1990&yr_renovated=2010&postal_code=52345&lat=45.9516307&long=-66.6493478&price=300000')
assert json.loads(response.text) == {"estimate": 464345, "actual": 0}, "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting missing arguments...")
response = requests.get('http://localhost:5000/get-house-price-test')
assert json.loads(response.text) == {"estimate": 0, "actual": 0}, "Test failed!"
print("\t\t\tTest passed!")

print("\tTesting '/get-ai-args' route...")
response = requests.get('http://localhost:5000/get-ai-args-test')
assert json.loads(response.text) == ["bedrooms","bathrooms","sqft_living","sqft_lot","floors","yr_built","yr_renovated","postal_code","lat","long"], "Test failed!"
print("\t\tTest passed!")
