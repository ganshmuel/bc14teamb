from typing import List, Dict
from flask import Flask,render_template, redirect, url_for, request, Response
import mysql.connector
import json
import datetime

app = Flask(__name__)


def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'Weights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Weights')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route ('/weight')
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
#    cur = mysql.connection.cursor()
#    cur.execute("""SELECT * FROM student_data WHERE id = %s""", (id,))
    return f"from{frm}to{to}filter{filter}"
    
@app.route ('/weight',methods=['POST'])
def post_weight():
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return
    
@app.route('/health')
def health():
    response = Response(status=200)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
