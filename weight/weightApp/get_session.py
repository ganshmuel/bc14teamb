from flask import Flask, Response, jsonify
import mysql
import mysql.connector


app = Flask(__name__,)
mydb = mysql.connector.connect(  # db configuration
    host="db",
    user="root",
    password="root",
    database="weight"
)



@app.route('/session/<id>', methods=['GET'])
def get_session(id):
        cursor = mydb.cursor()
        cursor.execute("use weight")
        try:
            cursor.execute("SELECT direction FROM transactions WHERE id = (%s)" % (id))
            record = cursor.fetchone()
            direction=str(record[0])
            if direction == "in":
                cursor.execute("SELECT id,truck,bruto FROM transactions WHERE id = (%s)" % (id))
                record = cursor.fetchall()
                json_data=[]
                for result in record:
                    d=dict()
                    d['id']=result[0]
                    d['truck']=result[1]
                    d['bruto']=result[2]
                    json_data.append(d)
                results_toload = []
                results_toload = jsonify(json_data)
                return results_toload          
            elif direction == "out":
                cursor.execute("SELECT id,truck,bruto,truckTara,neto,produce FROM transactions WHERE id = (%s)" % (id))
                record = cursor.fetchall()
                json_data=[]
                for result in record:
                    d=dict()
                    d['id']=result[0]
                    d['truck']=result[1]
                    d['bruto']=result[2]
                    d['truckTara']=result[3]
                    d['neto']=result[4]
                    json_data.append(d)
                results_toload = []
                results_toload = jsonify(json_data)
                return results_toload    
            else:
                return Response("direction unkown ", status=404, mimetype="text")
        except:
            return Response("id unkown", status=404, mimetype="text")