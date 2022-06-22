#!/usr/bin/env python3

import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
import mysql.connector
from os import path
from openpyxl import load_workbook

app = Flask(__name__)
api = Api(app)

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

def stringValidator(string):
    if not string:
        raise ValueError("Must not be empty string")
    if len(string) > 255:
        raise ValueError("Must not be longer then 255 charecters")
    return string


class HealthGet(Resource):
    def get(self):
        return {"message": 'OK'}, 200


class ProviderPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, nullable=False, type=stringValidator)
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
            return {"id":f"{cursor.lastrowid}"}
        else:
            return {"message":'This provider exists in our system'}, 400

class Rates(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', required=True, nullable=False, type=stringValidator)
    def post(self):
        args = self.parser.parse_args()
        fileName = args['file']
        file = f'{os.getcwd()}/in/{fileName}.xlsx'
        if path.exists(file):
            wb = load_workbook(file)
            ws = wb.active
            wb.save(file)
            fileData = tuple(ws.rows)
            for i in range(1, len(fileData)):
                product_id = fileData[i][0].value
                rates = fileData[i][1].value
                scope = fileData[i][2].value

                sql_where= f"SELECT * FROM Rates WHERE product_id ='{product_id}' AND scope ='{scope}'"
                cursor.execute(sql_where)
                isAlreadyExist = cursor.fetchone()
                lineData = (product_id, rates, scope)
                if isAlreadyExist == None:
                    sql_insert= "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, lineData)
                    dbConnect.commit()
                else:
                    sql_update = f"UPDATE Rates SET rate ='{rates}' WHERE product_id ='{product_id}' AND scope ='{scope}'"
                    cursor.execute(sql_update)
                    dbConnect.commit()
            return {"message":f'Rates from {fileName}.xlsx was updated in DB successfully'}, 200
            
        else:
            return {"message":f'{fileName}.xlsx not exist, please provide existing excel file.'}, 400 

    def get(self):
        return {"message":'get rates route'}, 200

api.add_resource(HealthGet, '/', '/health')
api.add_resource(ProviderPost, '/provider')
api.add_resource(Rates,'/rates')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
