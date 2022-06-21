#!/usr/bin/env python3

from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

dbConnect = mysql.connector.connect(
    # host=db refers to the mysql container, do not change it
    host="db",
    port=3306,
    user="root",
    password="password",
    database="billdb",
    auth_plugin="mysql_native_password"
)

cursor = dbConnect.cursor()

def nameValidator(name):
    if not name:
        raise ValueError("Must not be empty string")
    if len(name) > 255:
        raise ValueError("Must not be longer then 255 charecters")
    return name


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, nullable=False, type=nameValidator)


class HealthGet(Resource):
    def get(self):
        return Response('OK', status=200, mimetype='text')


class ProviderPost(Resource):
    def post(self):
        args = parser.parse_args()
        name = name=args['name']

        sql_search_name = f"SELECT name FROM Provider WHERE name = '{name}'"
        cursor.execute(sql_search_name)
        isNameExists = cursor.fetchone()
        if isNameExists == None:
            sql_insert_name = "INSERT INTO Provider (name) VALUES (%s)"
            val_name = [(name)]
            cursor.execute(sql_insert_name, val_name)
            dbConnect.commit()
            print(cursor.lastrowid, f"{cursor.rowcount} Provider inserted.")
            return {"id": f"{cursor.lastrowid}"}
        else:
            return Response('This provider exists in our system', status=400, mimetype='text')



api.add_resource(HealthGet, '/', '/health')
api.add_resource(ProviderPost, '/', '/provider')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
