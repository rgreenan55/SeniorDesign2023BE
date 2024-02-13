import requests
import json

print("Testing Endpoints...")
print("\tTesting '/get-house-price-by-address' route...")
print("\t\tTesting valid address...")
print("\t\t\tTest skipped!")
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
response = requests.get('http://localhost:5000/get-house-price?MedInc=-0.4587930058578523&HouseAge=1.459896251818046&AveRooms=-0.4109222676406087&Latitude=-0.8776422143928831&Longitude=0.6970911620892798&price=1.927')
assert json.loads(response.text)["estimate"] > 100000, "Test failed!"
print("\t\t\tTest passed!")
print("\t\tTesting missing arguments...")
response = requests.get('http://localhost:5000/get-house-price')
assert json.loads(response.text)["estimate"] > 0, "Test failed!"
print("\t\t\tTest passed!")

print("\tTesting '/get-ai-args' route...")
response = requests.get('http://localhost:5000/get-ai-args')
assert json.loads(response.text) == ["MedInc", "HouseAge", "AveRooms", "Latitude", "Longitude"], "Test failed!"
print("\t\tTest passed!")