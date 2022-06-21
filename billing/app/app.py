#!/usr/bin/env python3

from flask import Flask, Response, request
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)

mydb = mysql.connector.connect(
    host="db",
    user="root",
    password="password",
    database="billdb",
    auth_plugin='mysql_native_password'
    )

# Routes Section
def createProvider(name: str):
    if name != None or name != "":
        print("hello")
        # isProviderExist = Provider.query.filter_by(providerName=name).first()
        # if isProviderExist is None:
        #     newProvider = Provider(providerName=name)
        #     db.session.add(newProvider)
        #     db.session.commit()
        #     return Response({"id": newProvider.id}, status=200, mimetype='application/json')
        # else:
        #     return Response('400 Bad Request: This provider name is already exist!', status=400, mimetype='text')
    else:
        return Response('400 Bad Request: Please pass a valid provider name!', status=400, mimetype='text')


@app.route("/health", methods=["GET"])
def health():
    return Response('OK', status=200, mimetype='text')


@app.route("/provider", methods=["POST"])
def provider():
    data = request.json
    dbRes = createProvider(data["name"])
    return dbRes


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
