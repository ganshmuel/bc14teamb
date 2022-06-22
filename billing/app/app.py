#!/usr/bin/env python3

import os
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import mysql.connector
from os import path
from openpyxl import load_workbook
import shutil

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

cursor = dbConnect.cursor(buffered=True)


def nameValidator(name):
    if not name:
        raise ValueError("Must not be empty string")
    if len(name) > 255:
        raise ValueError("Must not be longer then 255 charecters")
    return name


def providerIdValidator(provider_id):
    if not provider_id:
        raise ValueError("Must not be empty provider_id")
    if int(provider_id) < 10000 and int(provider_id) >999999999 :
        raise ValueError("Must not be >= 10000")
    return provider_id


def truckLicenseValidator(name):
    if not name:
        raise ValueError("Must not be empty string")
    if len(name) > 255:
        raise ValueError("Must not be longer then 255 charecters")
    return name


def isProviderIdInDb(provider_id):


    sql_search_id = f"SELECT name FROM Provider WHERE id = '{provider_id}'"
    cursor.execute(sql_search_id)
    isNameExists = cursor.fetchone()
    if isNameExists is None:
        return False
    return True

def isTruckIdInDb(truck_id):
    sql_search_id = f"SELECT * FROM Trucks WHERE id = '{truck_id}'"
    cursor.execute(sql_search_id)
    if cursor.fetchone() is None:
        return False
    return True


class HealthGet(Resource):
    def get(self):
        try:
            dbConnect.is_connected()
        except mysql.connector.errors.InterfaceError:
            return {'message': 'Server error, contact your Michael'}, 500
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
            return {"id": f"{cursor.lastrowid}"}
        else:
            return {"message": 'This provider exists in our system'}, 400


class Rates(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', required=True, nullable=False, type=nameValidator)

    def post(self):
        args = self.parser.parse_args()
        fileName = args['file']
        file = f'{os.getcwd()}/in/{fileName}.xlsx'
        if path.exists(file):
            f = open(f'{os.getcwd()}/in/last-file.txt', 'w')
            f.write(file)
            f.close()
            wb = load_workbook(file)
            ws = wb.active
            wb.save(file)
            fileData = tuple(ws.rows)
            for i in range(1, len(fileData)):
                product_id = fileData[i][0].value
                rates = fileData[i][1].value
                scope = fileData[i][2].value

                sql_where = f"SELECT * FROM Rates WHERE product_id ='{product_id}' AND scope ='{scope}'"
                cursor.execute(sql_where)
                isAlreadyExist = cursor.fetchone()
                lineData = (product_id, rates, scope)
                if isAlreadyExist == None:
                    sql_insert = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, lineData)
                    dbConnect.commit()
                else:
                    sql_update = f"UPDATE Rates SET rate ='{rates}' WHERE product_id ='{product_id}' AND scope ='{scope}'"
                    cursor.execute(sql_update)
                    dbConnect.commit()
            return {"message": f'Rates from {fileName}.xlsx was updated in DB successfully'}, 200

        else:
            return {"message": f'{fileName}.xlsx not exist, please provide existing excel file.'}, 400

    def get(self):
        lastFileLocation = open(f'{os.getcwd()}/in/last-file.txt', "r")
        lastFile = lastFileLocation.read()
        lastFileLocation.close()
        fileCopy = f"{os.getcwd()}/in/last_rates_file.xlsx"
        shutil.copy(lastFile, fileCopy)
        return {"message":'last_rates_file.xlsx was generated'}, 200

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
    parser.add_argument('provider_id', required=True, nullable=False, type=providerIdValidator)
    parser.add_argument('id', required=True, nullable=False)


    def post(self):
        args = self.parser.parse_args()
        provider_id = args['provider_id']

        truck_id = args['id']
        if isProviderIdInDb(provider_id) is False:
            return Response("This provider doesn't exist in our system", status=400, mimetype='json')
        if isTruckIdInDb(truck_id) is True:
            return Response("This truck is already  in our system", status=400, mimetype='json')

        sql_insert_name = "INSERT INTO Trucks (id, provider_id) VALUES (%s, %s)"
        val = (truck_id, provider_id)
        cursor.execute(sql_insert_name, val)
        dbConnect.commit()
        return Response('Ok', status=200, mimetype='json')


api.add_resource(TruckPost, '/truck/')
api.add_resource(HealthGet, '/health')
api.add_resource(ProviderPost, '/provider/')
api.add_resource(ProviderPut, '/provider/<provider_id>')
api.add_resource(Rates, '/rates')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_port, debug=False)
