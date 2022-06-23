from flask import Flask, jsonify, request
import mysql
import mysql.connector
import datetime


app = Flask(__name__,)
mydb = mysql.connector.connect(  # db configuration
    host="db",
    user="root",
    password="root",
    database="weight"
)


@app.route('/weight', methods=['GET'])
def get_weight():
    frm = request.args.get('from')
    to = request.args.get('to')
    filter = request.args.get('filter')
    if frm == None:
        frm = datetime.datetime.now().strftime("%Y%m%d000000")
    if to == None:
        to = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if filter == None:
        filter = "in,out,none"
    fltr = filter.split(",")
    where_in = ','.join(['%s'] * len(fltr))
    mycursor = mydb.cursor()  # Connecting to database and getting cursor
    mycursor.execute("use weight")  
    # SELECT * FROM transactions WHERE datetime >= 2022063000000 AND datetime <= 20220630123456 and direction in ('in','out','none');
    sql = ("SELECT * FROM transactions WHERE datetime >= (%s) AND datetime <= (%s) AND direction IN (%s) " %
           (frm, to, where_in))
    mycursor.execute(sql, fltr)
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    json_data=[]
    for result in myresult:
        d=dict()
        d['id']=result[0]
        d['datetime']=result[1]
        d['direction']=result[2]
        d['truck']=result[3]
        d['containers']=result[4]
        d['bruto']=result[5]
        d['truckTara']=result[6]
        d['neto']=result[7]
        d['produce']=result[8]
        json_data.append(d)
    results_toload = []
    results_toload = jsonify(json_data)
    return results_toload