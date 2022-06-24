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
    x = mycursor.execute("SELECT container_id FROM registered_containers WHERE weight ISNULL")
    myresult = str(mycursor.fetchall())
    return myresult

app = Flask(__name__,)