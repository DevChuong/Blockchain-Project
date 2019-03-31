from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
url = "http://localhost:3000/users"
r = requests.get(url)
result = r.json()

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, name):
        for user in result:
            if(name == user["name"]):
                return user,200
        return "User not found",404