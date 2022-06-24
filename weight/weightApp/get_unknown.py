from flask import Flask, render_template 
import mysql
import mysql.connector


app = Flask(__name__,)


mydb = mysql.connector.connect(  # db configuration
    host="db",
    user="root",
    password="root",
    database="weight"
)

@app.route('/unknown/', methods=['GET'])
def unknown_containers():
    mycursor = mydb.cursor()
    x = mycursor.execute("SELECT container_id FROM containers_registered WHERE weight IS NULL")
    print("hello")
    return x

app = Flask(__name__,)