import requests
import json

print("Testing Endpoints...")
print("\tTesting '/get-assessment-by-arguments' route...")
print("\t\tTesting valid arguments...")
response = requests.get("http://localhost:5000/get-assessment-by-arguments?latitude=45.3724494&longitude=-75.7798211&yearBuilt=2016.0&bedrooms=1.0&bathrooms=1.0&garage=0.0&lotDepth=31.045&lotFrontage=13.895&postalCode=488.0&propertyType=1.0&style=0.0&price=349900.0")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['actual'] == 349900.0, "Invalid actual value"
assert resJson['estimate'] >= 1000.0, "Invalid predicted value"
print("\t\t\tTest passed!")

print("\t\tTesting missing arguments...")
response = requests.get("http://localhost:5000/get-assessment-by-arguments")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['actual'] == 0, "Invalid actual value"
assert resJson['estimate'] >= 1000.0, "Invalid predicted value"
print("\t\t\tTest passed!")


print("\tTesting '/get-assessment-by-address' route...")
print("\t\tTesting valid address...")
response = requests.get("http://127.0.0.1:5000/get-assessment-by-address?address=1466 Launay Avenue, Ottawa, Ontario")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['actual'] == 399900.0, "Invalid actual value"
assert resJson['estimate'] >= 1000.0, "Invalid predicted value"
print("\t\t\tTest passed!")

print("\t\tTesting invalid address...")
response = requests.get("http://127.0.0.1:5000/get-assessment-by-address?address=Not A Real Address")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['error'] == "true", "Invalid error value"
assert resJson["reason"] == "House Not Available", "Invalid reason value"
print("\t\t\tTest passed!")

print("\t\tTesting missing address...")
response = requests.get("http://127.0.0.1:5000/get-assessment-by-address?address=")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['error'] == "true", "Invalid error value"
assert resJson["reason"] == "No address provided", "Invalid reason value"
print("\t\t\tTest passed!")

print("\t\tTesting missing address parameter...")
response = requests.get("http://127.0.0.1:5000/get-assessment-by-address")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson['error'] == "true", "Invalid error value"
assert resJson["reason"] == "No address provided", "Invalid reason value"
print("\t\t\tTest passed!")


print("\tTesting '/get-all-addresses' route...")
print("\t\tTesting valid address count...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert len(resJson) != 194, "Address count changed"
print("\t\t\tTest passed!")


print("\tTesting '/get-all-addresses-by-prefix' route...")
print("\t\tTesting valid prefix with 1 result...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses-by-prefix?prefix=1466")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert len(resJson) == 1, "Invalid address count"
print("\t\t\tTest passed!")

print("\t\tTesting valid prefix with multiple results...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses-by-prefix?prefix=14")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert len(resJson) == 3, "Invalid address count"

print("\t\tTesting invalid prefix...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses-by-prefix?prefix=Not A Real Prefix")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert len(resJson) == 0, "Invalid address count"
print("\t\t\tTest passed!")

print("\t\tTesting no prefix...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses-by-prefix?prefix=")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert len(resJson) >= 190, "Invalid address count"
print("\t\t\tTest passed!")

print("\t\tTesting missing prefix parameter...")
response = requests.get("http://127.0.0.1:5000/get-all-addresses-by-prefix")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert resJson["error"] == "No prefix provided", "Invalid address count"
print("\t\t\tTest passed!")


print("\tTesting '/get-random-address-and-attributes' route...")
print("\t\tTesting valid result...")
response = requests.get("http://127.0.0.1:5000/get-random-address-and-attributes")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert "address" in resJson, "Address not found"
assert "attributesObj" in resJson, "Attributes not found"
assert "lat" in resJson, "Latitude not found"
assert "lng" in resJson, "Longitude not found"
print("\t\t\tTest passed!")


print("\tTesting '/get-random-address-and-attributes-with-results' route...")
print("\t\tTesting valid result...")
response = requests.get("http://127.0.0.1:5000/get-random-address-and-attributes-with-results")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert "house" in resJson, "house not found"
assert "results" in resJson, "results not found"
print("\t\t\tTest passed!")


print("\tTesting '/get-AI-accuracy' route...")
print("\t\tTesting valid result...")
response = requests.get("http://127.0.0.1:5000/get-AI-accuracy")
assert response.status_code == 200, "Invalid status code"
resJson = response.json()
assert "accuracy" in resJson, "accuracy not found"
print("\t\t\tTest passed!")


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