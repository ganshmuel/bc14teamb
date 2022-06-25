import mysql
import mysql.connector
from flask import Flask, render_template, Response, jsonify, request 


mydb = mysql.connector.connect(  # db configuration
        host="db",
        user="root",
        password="root",
        database="weight",

    )

def first_table():
    cursor = mydb.cursor()
    cursor.execute("use weight")
    cursor.execute("SHOW COLUMNS FROM transactions")      
    col = list(cursor.fetchall())
    cursor.execute("select  * FROM transactions")
    rows= list(cursor.fetchall())
    l=[]
    for i in col:
        l.append(i[0])
    c=[l]+rows
    return c
def second_table():
    cursor = mydb.cursor()
    cursor.execute("use weight")
    cursor.execute("SHOW COLUMNS FROM containers_registered")      
    col = list(cursor.fetchall())
    cursor.execute("select  * FROM containers_registered")   
    rows= list(cursor.fetchall())
    l=[]
    for i in col:
        l.append(i[0])
    c=[l]+rows
    return c