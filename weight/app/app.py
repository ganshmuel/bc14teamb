from typing import List, Dict
from flask import Flask,render_template, redirect, url_for, request, Response
import mysql.connector
import json

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
    request.form['']
    

@app.route('/health')
def health():
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
