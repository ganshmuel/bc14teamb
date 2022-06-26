from flask import Flask, Response, request
import mysql
import mysql.connector
import csv, json

app = Flask(__name__,)
mydb = mysql.connector.connect(  # db configuration
    host="db",
    user="root",
    password="root",
    database="weight"
)

@app.route('/batch-weight', methods=['POST'])
def post_batch():
    cursor = mydb.cursor()
    cursor.execute("use weight")  
    dict_list = list()
    file = '/in/'
    file = file + request.args.get('file')
    if file.endswith('.csv'):
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            unit = next(reader)[1]
            for line in reader:
                dict_list.append({'container_id':line[0],'weight':line[1],'unit':unit})
        for item in dict_list:
            try:
                cursor.execute("insert into containers_registered(container_id, weight, unit) values(%s, %s, %s)", (item['container_id'], item['weight'], item['unit']))
                mydb.commit
            except:
                return "Duplicate entry"
            return "OK"
    elif file.endswith('.json'):
        json_data=open(file).read()
        json_obj = json.loads(json_data)
        for item in json_obj:
            cursor.execute("insert into containers_registered(container_id, weight, unit) values(%s, %s, %s)", (item['id'], item['weight'], item['unit']))
            mydb.commit
        return "json OK"
    else:
        return Response("ID NOT FOUND", status=404, mimetype="text")