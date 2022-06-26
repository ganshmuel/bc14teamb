from flask import Flask, Response, jsonify, request
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


@app.route('/weight', methods=['POST'])
def post_weight():
    direction = str(request.form['direction'])
    truck = str(request.form['truck'])
    containers = str(request.form['containers'])    
    weight = int(request.form['weight'])
    unit = str(request.form['unit'])
    produce = str(request.form['produce'])
    force = str(request.form['force'])
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if unit == "lbs":
        weight = weight*0.45
    mycursor = mydb.cursor()
    mycursor.execute("SELECT direction FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
    direction_check = mycursor.fetchone()
    if direction_check is not None and direction_check[0] is not None:
        direction_check = direction_check[0]
    if direction == "in" or direction == "none":
        bruto = weight
        mycursor.execute("SELECT id FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
        id = mycursor.fetchone()
        if id is not None and id[0] is not None:
            id = id[0]
        if direction_check == "in" and direction == "in":
            if force == "false":
                #if force=false will generate an error
                return Response("Error duplicate entry (maybe use force=True)", status=404, mimetype="text")
            elif force == "true":
                #will over-write db
                mycursor.execute("UPDATE transactions SET bruto = '%s' WHERE id = '%s'" , (bruto , id))
                mycursor.execute("SELECT * FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
                myresult = mycursor.fetchall()
                json_data=[]
                for result in myresult:
                    d=dict()
                    d['id']=result[0]
                    d['truck']=result[3]
                    d['bruto']=result[5]
                    json_data.append(d)
                results_toload = []
                results_toload = jsonify(json_data)
                return results_toload
            else:
                return Response("Unknown value of 'force'", status=404, mimetype="text")
        elif direction == "none" and direction_check == "in":
            #"none" after "in" will generate error
            return Response("Error none after in ", status=404, mimetype="text")
        else:
            mycursor.execute("INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (%s, %s, %s, %s, %s, %s)", (date, direction, truck, containers, bruto, produce))
            mycursor.execute("SELECT * FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
            myresult = mycursor.fetchall()
            json_data=[]
            for result in myresult:
                d=dict()
                d['id']=result[0]
                d['truck']=result[3]
                d['bruto']=result[5]
                json_data.append(d)
            results_toload = []
            results_toload = jsonify(json_data)
            return results_toload
    elif direction == "out":
        contsum = 0
        if containers:#  calculate truckTara
            contlist = containers.split(",")
            
            for c in contlist: # calculate containers tara weight
                mycursor.execute("SELECT weight FROM containers_registered WHERE container_id = '%s'" % (c))
                contweight = mycursor.fetchone()
                if contweight is not None and contweight[0] is not None:
                    contweight = int(contweight[0])
                    contsum = contsum + contweight
            truckTara = weight - contsum
        else: #calculate truckTara
            truckTara = weight
       ############################# get bruto from DB , neto = bruto - truckTara - contsum
        mycursor.execute("SELECT bruto FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
        bruto = mycursor.fetchone()      ###record = mycursor.fetchone()
        if bruto is not None and bruto[0] is not None:
            bruto = bruto[0]
        mycursor.execute("SELECT id FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
        id = mycursor.fetchone()
        if id is not None and id[0] is not None:
            id = id[0]
        ##### DONT FORGET TO IMPLEMENT CALCULATIONS FOR CONTAINERS IN PREVIOUS IN FOR NETO IN  OUT
        mycursor.execute("SELECT containers FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
        contnrs = mycursor.fetchone()
        if contnrs is not None and contnrs[0] is not None:
            contnrs = contnrs[0]
            contlist = contnrs.split(",")
        for c in contlist: # calculate containers tara weight
                mycursor.execute("SELECT weight,unit FROM containers_registered WHERE container_id = '%s'" % (c))
                record = mycursor.fetchone()
                if record:
                    cont_weight=record[0] 
                    if record[1]=="lbs" :
                        cont_weight*=0.45
                    contsum = int(contsum + cont_weight)
        neto = float(bruto) - int(truckTara) - int(contsum)
        if direction_check == direction:
            if force == ("False" or "false"):
                #if force=false will generate an error
                return Response("Error", status=404, mimetype="text")
            elif force == ("true" or "True"):#will over-write db
                mycursor.execute("SELECT id FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
                id = mycursor.fetchone()
                if id is not None and id[0] is not None:
                    id = id[0]
                mycursor.execute("UPDATE transactions SET bruto='%s' , neto='%s' , truckTara='%s' WHERE id = (%s)" , (weight , neto , truckTara , id))
                mycursor.execute("SELECT * FROM transactions WHERE truck = '%s' ORDER BY id DESC LIMIT 1" % (truck))
                myresult = mycursor.fetchall()
                json_data=[]
                for result in myresult:
                    d=dict()
                    d['id']=result[0]
                    d['truck']=result[3]
                    d['bruto']=result[5]
                    d['truckTara']=result[6]
                    d['neto']=result[7]
                    json_data.append(d)
                results_toload = []
                results_toload = jsonify(json_data)
                return results_toload
        if direction_check != "in":
                #"out" without an "in" will generate error
                return Response(f"Error out without in {direction_check}", status=404, mimetype="text")
        mycursor.execute("INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce, neto, truckTara ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (date, direction, truck, containers, weight, produce,neto , truckTara ))
        #######mydb.commit        
        last_insert = mycursor.lastrowid
        mycursor.execute("SELECT * FROM transactions WHERE id = '%s'", (last_insert))
        myresult = mycursor.fetchall()
        json_data=[]
        for result in myresult:
            d=dict()
            d['id']=result[0]
            d['truck']=result[3]
            d['bruto']=result[5]
            d['truckTara']=result[6]
            d['neto']=result[7]
            json_data.append(d)
        results_toload = []
        results_toload = jsonify(json_data)
        return results_toload
    else:
        return Response(f"Unknown Error", status=404, mimetype="text")