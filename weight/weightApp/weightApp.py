import sqlite3 as sql
from flask import Flask, render_template, Response, jsonify, request
from typing import List, Dict
import mysql
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(  # db configuration
        host="db",
        user="root",
        password="root",
        database="weight"
    )

def add_data(title, content):
    
    mycursor = mydb.cursor()# Connecting to database and getting cursor
    mycursor.execute("INSERT INTO transactions(title, content) VALUES (%s, %s)" % (title, content))  # Adding data to db
    mydb.commit()  # Applying changes
    return ""

def get_data():
    #  return all of the weightings and their info 
    #  from t1 to t2 (and direction!) in JSON format.
    mycursor = mydb.cursor()# Connecting to database and getting cursor
    mycursor.execute("use weight")
    mycursor.execute("SHOW COLUMNS FROM transactions")# Getting data from db. SELECT <column> from <table>
    myresult = str(mycursor.fetchall())
    return myresult

@app.route('/health')
def health():
    return Response("OK",status=200, mimetype="text")

@app.route('/weight', methods=['GET'])
def get():
    frm = request.args.get('from')
    to = request.args.get('to')
    filter = request.args.get('filter')
    if frm == None:
        frm = datetime.datetime.now().strftime("%Y%m%d000000")
    if to == None:
        to = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if filter == None:
        filter = "in,out,none"
    return get_data()
       
@app.route('/weight', methods=['POST'])
def insert():
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8081')