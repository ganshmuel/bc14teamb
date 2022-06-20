#!/usr/bin/env python3

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://billdb_app:CYuoYBprY4so@database-1.c62tpaoqyddb.us-east-1.rds.amazonaws.com:3621/billdb"
app.config["SERVER_NAME"] = "0.0.0.0"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    providerName = db.Column(db.String(255), unique=True, nullable=False)

def createProvider(name: str):
    if name is None or name == "":
        isProviderExist = Provider.query.filter_by(providerName=name).first()
        if isProviderExist is None:
            newProvider = Provider(providerName=name)
            db.session.add(newProvider)
            db.session.commit()
            return Response({"id": newProvider.id}, status=200, mimetype='application/json')
        else:
            return Response('400 Bad Request: This provider name is already exist!', status=400, mimetype='text')
    else:
        return Response('400 Bad Request: Please pass a valid provider name!', status=400, mimetype='text')

@app.route("/health", methods=["GET"])
def health():
    return Response('OK', status=200, mimetype='text')

@app.route("/provider/<name>", methods=["POST"])
def provider(name):
    dbRes = createProvider(name)
    return dbRes

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)