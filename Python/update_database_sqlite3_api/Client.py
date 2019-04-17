import requests
import json
response = requests.put("http://127.0.0.1:5000/user/44A7D3?supervisor_rating=Good&feedback=Excellent")

print("Data added successfully.")