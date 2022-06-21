#!/usr/bin/env python3

from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

mydb = mysql.connector.connect(
    host="db",
    user="root",
    password="password",
    database="billdb",
    auth_plugin='mysql_native_password'
    )

def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, nullable=False, type=non_empty_string)

def createProvider(name: str):
    if name != None or name != "":
        print("hello")
    else:
        return Response('400 Bad Request: Please pass a valid provider name!', status=400, mimetype='text')

class HealthGet(Resource):
    def get(self):
        return Response('OK', status=200, mimetype='text')

class ProviderPost(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        return name

api.add_resource(HealthGet, '/', '/health')
api.add_resource(ProviderPost, '/', '/provider')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)