import sqlite3 as sql
from flask import Flask, render_template, Response, jsonify, request 
import os , csv , json 
from typing import List, Dict


# from requests import session
import mysql
import mysql.connector
from datetime import datetime

def item():
      mydb = mysql.connector.connect(  # db configuration
      host="db",
      user="root",
      password="root",
        database="weight",
        port= 3306,
      )
      id = request.args.get('id')
      t1 = request.args.get('t1')
      t2 = request.args.get('t2')
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



