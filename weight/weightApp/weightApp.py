import sqlite3 as sql
from flask import Flask, render_template, Response, jsonify, request
import mysql
import mysql.connector
import datetime , csv , os , json
from mysql.connector import FieldType
import show_tables

app = Flask(__name__,)
mydb = mysql.connector.connect(  # db configuration
    host="db",
    user="root",
    password="root",
    database="weight"
)

@app.route('/health')
def get_health():
    return Response("OK", status=200, mimetype="text")


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/weight', methods=['POST'])
def post_weight():
    direction = str(request.form['direction'])
    truck = str(request.form['truck'])
    containers = str(request.form['containers'])    
    bruto = int(request.form['bruto'])
    produce = str(request.form['produce'])
    force = bool(request.form['force'])
    neto = int(request.form['neto'])
    truckTara = int(request.form['truckTara'])
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    mycursor = mydb.cursor()
    if direction == ("in" or "none"):
        direction_check = mycursor.execute("SELECT direction WHERE truck = (%s) ORDER BY id DESC LIMIT 1", (truck))
        id = mycursor.execute("SELECT id WHERE truck = (%s) ORDER BY id DESC LIMIT 1", (truck))
        if direction_check == direction:
            if force == "False":
                #if force=false will generate an error
                return Response("Error", status=404, mimetype="text")
            elif force == "True":
                #will over-write db
                mycursor.execute("UPDATE transactions SET bruto = %s WHERE id = %s" , (bruto , id))
        elif direction == "none" and direction_check == "in":
            #"none" after "in" will generate error
            return Response("Error", status=404, mimetype="text")
        mycursor.execute("INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (%s, %s, %s, %s, %s, %s)",
                        (date, direction, truck, containers, bruto, produce))
        mydb.commit
    elif direction == "out":
        if direction_check == direction:
            if force == "False":
                #if force=false will generate an error
                return Response("Error", status=404, mimetype="text")
            elif force == "True":
                #will over-write db
                mycursor.execute("UPDATE transactions SET bruto = %s , neto = %s , truckTara = %s WHERE id = %s" , (bruto , neto , truckTara , id))
        if direction_check != "in":
                #"out" without an "in" will generate error
                return Response("Error", status=404, mimetype="text")
        mycursor.execute("INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce, neto, truckTara ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (date, direction, truck, containers, bruto, produce,neto , truckTara ))
    else:
        return Response("Error", status=404, mimetype="text")


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
            cursor.execute("insert into containers_registered(container_id, weight, unit) values(%s, %s, %s)", (item['container_id'], item['weight'], item['unit']))
            mydb.commit
        return "OK"
    elif file.endswith('.json'):
        json_data=open(file).read()
        json_obj = json.loads(json_data)
        for item in json_obj:
            cursor.execute("insert into containers_registered(container_id, weight, unit) values(%s, %s, %s)", (item['id'], item['weight'], item['unit']))
            mydb.commit
        return "json OK"
    else:
        return Response("Not Found", status=404, mimetype="text")

  

@app.route('/session/<id>', methods=['GET'])
def get_session(id):
    cursor = mydb.cursor()
    cursor.execute("use weight")
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
            # d['truckTara']=result[6]
            # d['neto']=result[7]
            # d['produce']=result[8]
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
        return Response("Not Found", status=404, mimetype="text")

@app.route('/unknown/', methods=['GET'])
def unknown_containers():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT container_id FROM containers_registered WHERE weight IS NULL")
    x = mycursor.fetchall()
    y = ''.join(''.join(tup) for tup in x)
    return y



@app.route('/item/<id>/', methods=['GET'])
def item(id):
    #   id = request.args.get('id')
      t1 = request.args.get('t1')
      t2 = request.args.get('t2')
      b=item1(id, t1, t2) 
      if b=="id not exist - should be 404 error " :
        return Response("Error", status=404, mimetype="text")
      json_object = json.dumps(b, indent = 4) 
    #   print("\n\ntype of returned object")
    #   print(type(json_object))
      return  (json_object)


def item1(id, t1, t2):
    #   id = request.args.get('id')
    #   t1 = request.args.get('t1')
    #   t2 = request.args.get('t2')
      print("\n\n t1 is %s  and t2 is %s"  %(t1,t2) )

      if  not t1   : t1=datetime.now().strftime("%Y%m01000000")
      if  not t2   : t2=datetime.now().strftime("%Y%m%d%H%M%S")
      cursor = mydb.cursor()
      print("\n\n t1 is %s  and t2 is %s"  %(t1,t2) )
      query="select  id,truckTara,truck ,datetime FROM transactions where truck=(%s) "
      # query="select  id FROM transactions where truck=(%s)"
      cursor.execute(query,(id,) )                                        #search truck id
      firstresult=cursor.fetchall()    #first result is type list
      
      last_tara_time="0"


      if firstresult:
        print("first result is %s" %firstresult)
        truck_sessions=[]
        for i in firstresult:
            if i[3]>t1 and i[3]<t2:
               truck_sessions.append(i[0])      ##append the row number (primary key) to ssesions
            if i[3] > last_tara_time and i[1]!="na":
               last_tara_time=i[3]
               tr_tara=i[1]

        print("truck session is: %s" %truck_sessions)
        last_time="0"
        if not tr_tara: tr_tara="na"
           
        return({"id":id ,"tara":tr_tara,"sessions":truck_sessions })
###############################################################################################      
      #next  blocks will  search id at containers field if id was not a truck id .

      # query="select id,containers  FROM transactions WHERE datetime > (%s) AND datetime < (%s)" 
      query="select id,containers,datetime  FROM transactions "   
  
      cursor.execute(query,)
      s_result=cursor.fetchall()

      cont_sessions=[]
      cont_exist=False

      for i in s_result:
      #   # if id in (i[1].split(",")): cont_sessions.append(i[0])
        if id in ("".join(i[1].split(" "))).split(","): 
              if (i[2]>t1) and i[2]<t2 :
                 cont_sessions.append(i[0])
              cont_exist=True
      # print("cont sessin is: %s" %cont_sessions)
      if cont_exist==True:
          # get container weight
        query="select weight,unit  FROM containers_registered where container_id=%s"   # search id at containers
        cursor.execute(query,(id,))
        cont_tara=cursor.fetchall()
        if cont_tara:
            cont_weight=cont_tara[0][0] 
            if cont_tara[0][1]=="lbs" :
              cont_weight*=0.453
              cont_weight=int(cont_weight)
        else: cont_weight="na"

      #################################################

      if cont_exist==False:   # next block exec if containers is not on session but is on containers_registers  table
           query="select weight,unit  FROM containers_registered where container_id=%s"   # search id at containers
           cursor.execute(query,(id,))
           cont_tara=cursor.fetchall()
           if cont_tara:
              cont_weight=cont_tara[0][0] 
              if cont_tara[0][1]=="lbs" :
                cont_weight*=0.453
                cont_weight=int(cont_weight)
              else: cont_weight="na"
              return ({'id':str(id) , 'tara':cont_weight ,'sessions':[] })
           return "id not exist - should be 404 error "
      else:
         return ({'id':str(id) , 'tara':cont_weight ,'sessions':cont_sessions })


@app.route('/st')
def st():
   c=show_tables.first_table()
   d=show_tables.second_table()
   return render_template('tables.html',c=c, gg=d )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8081')
