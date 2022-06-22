#!/usr/bin/env python3

from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import mysql.connector
import os

app = Flask(__name__)
api = Api(app)

# INTERNAL_APP_PORT is defined in the Dockerfile
app_port = os.getenv('INTERNAL_APP_PORT')

dbConnect = mysql.connector.connect(
    # host=db refers to the mysql container, do not change it
    host="db",
    port=3306,
    user="billdb_owner",
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


def providerIdValidator(provider_id):
    if not provider_id:
        raise ValueError("Must not be empty provider_id")
    if int(provider_id) < 10000:
        raise ValueError("Must not be >= 10000")
    return provider_id

#return id or None
def getProviderIdInDb(provider_id):
    sql_search_name = f"SELECT name FROM Provider WHERE id = '{provider_id}'"
    cursor.execute(sql_search_name)
    one = cursor.fetchone()
    print(one)
    print(cursor.lastrowid)
    return cursor.lastrowid



class HealthGet(Resource):
    def get(self):
        return {'message': 'OK'}, 200


class ProviderPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, nullable=False, type=nameValidator)

    def post(self):
        args = self.parser.parse_args()
        name = args['name']
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


class ProviderPut(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, nullable=False, type=nameValidator)

    def put(self, provider_id):
        args = self.parser.parse_args()
        name = args['name']

        sql = f"SELECT id FROM Provider WHERE id = '{provider_id}'"
        cursor.execute(sql)
        out = cursor.fetchone()
        if out == None:
            return Response("Provider with this id doesn' exists ", status=400, mimetype='text')

        sql = f"SELECT name FROM Provider WHERE name = '{name}'"
        cursor.execute(sql)
        out = cursor.fetchone()
        if out != None:
            return Response('Provider with this name already exists ', status=400, mimetype='text')
        sql = "UPDATE Provider SET name = %s WHERE id = %s"
        val = (name, provider_id)
        cursor.execute(sql, val)
        dbConnect.commit()
        return {"id": provider_id, "new_name": name}



class TruckPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('provider_id', required=True, nullable=False, type = providerIdValidator)

    def post(self):
        args = self.parser.parse_args()
        id = args['provider_id']
        provider_table_id  = getProviderIdInDb(id)
        return {"id": f"{provider_table_id}"}
        # truck_licence_plates = args['id']
        # sql = f"SELECT id FROM Provider WHERE id = '{provider_id}'"
        # cursor.execute(sql)
        # out = cursor.fetchone()
        # if out != None:
        #     return Response("Provider with this id doesn' exists.", status=400, mimetype='text')
        # sql_insert_name = "INSERT INTO Trucks (id, provider_id) VALUES (%s, %s)"
        # val = ([truck_licence_plates, provider_id])

api.add_resource(TruckPost, '/truck/')

api.add_resource(HealthGet, '/', '/health')
api.add_resource(ProviderPost, '/provider/')
api.add_resource(ProviderPut, '/provider/<provider_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_port, debug=True)
