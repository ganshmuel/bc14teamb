#!/usr/bin/env python3

import os
import requests
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import mysql.connector
from os import path
from openpyxl import load_workbook
import shutil
from datetime import datetime

WEIGHT_APP_BASE_URL = 'http://localhost:8081:'

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
            fileData = []
            for row in ws.rows:
                if row[0].value != None and row[1].value != None and row[2].value !=None:
                    fileData.append(row)  
            for i in range(1, len(fileData)):
                product_id = fileData[i][0].value
                rates = fileData[i][1].value
                scope = fileData[i][2].value
                if product_id != None or rates != None or scope != None:
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
                else:
                    return {"message": f"{fileName}.xlsx has missing values"}, 
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

class Bill(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('t1', type=str, location='args')
    parser.add_argument('t2', type=str, location='args')
    def get(self, provider_id):
        args = self.parser.parse_args()
        sql_search_name = f"SELECT name FROM Provider WHERE id = '{provider_id}'"
        cursor.execute(sql_search_name)
        provider = cursor.fetchone()
        if provider != None:
            if args['t1'] == None:
                startDate = datetime.strptime(datetime.today().replace(day=1,hour=0,minute=0,second=0).strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
            else:
                startDate = datetime.strptime(args['t1'], '%Y%m%d%H%M%S')
            if args['t2'] == None:
                endDate = datetime.strptime(datetime.now().strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
            else:
                endDate = datetime.strptime(args['t2'], '%Y%m%d%H%M%S')
            name = provider[0]
            sql_search_trucks = f"SELECT id FROM Trucks WHERE provider_id = '{provider_id}'"
            cursor.execute(sql_search_trucks)
            trucks = cursor.fetchall()
            numTrucks = len(trucks)
            if numTrucks != 0:
                return {
                "id":provider_id,
                "name": name,
                "from": f"{startDate}",
                "to": f"{endDate}", 
                "truckCount": numTrucks,
                }, 200
            else:
                return {"message":f"Provider with id: {provider_id} has no recorded trucks"}, 400
        else:
            return {"message":f"No provider exist with id: {provider_id}"}, 400
        

class UpdateProviderId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('provider_id', required=True, nullable=False, type=providerIdValidator)
    
    def put(self, truck_id):
        args = self.parser.parse_args()
        provider_id = args['provider_id']

        if isProviderIdInDb(provider_id) is False:
            return Response("This provider doesn't exist in our system", status=400, mimetype='json')
        if isTruckIdInDb(truck_id) is False:
            return Response("This truck doesn't exist in our system", status=400, mimetype='json')

        sql_update_provider = "UPDATE Trucks SET provider_id=%s WHERE id=%s" 
        val = (provider_id, truck_id)
        cursor.execute(sql_update_provider, val)
        dbConnect.commit()
        return Response('Ok', status=200, mimetype='json')

class TruckGet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', required=True, nullable=False)
    parser.add_argument('t1', type=str)
    parser.add_argument('t2', type=str)

    def get(self, id):
        args = self.parser.parse_args()
        if isTruckIdInDb(id) is False:
            return Response("The truck with this id doesn't exist", status=400, mimetype='text')
        else:
            t1 = args['t1']
            path = WEIGHT_APP_BASE_URL + '/item/' + id
            if t1 is None:
                return requests.get(path).content
            else:
                path = path + '/?from=' + t1
                t2 = args['t2']
                if t2 is None:
                    return requests.get(path).content
                else:
                    path = path + '&to =' +t2
                    return requests.get(path).content


api.add_resource(TruckPost, '/truck/')
api.add_resource(TruckGet, '/truck/<id>')
api.add_resource(HealthGet, '/health')
api.add_resource(ProviderPost, '/provider/')
api.add_resource(ProviderPut, '/provider/<provider_id>')
api.add_resource(Rates, '/rates')
api.add_resource(Bill, '/bill/<provider_id>')
api.add_resource(UpdateProviderId, '/trucks/<truck_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_port, debug=False)
