# 6A 19090019 Adi Sangjya
# 6A 19090011 Aida Nur Sya'bani
# 6A 19090097 Ika Bella Fitriani Putri
# 6A 19090098 Rizky Nafianto
from flask import Flask,request,jsonify
from flask_httpauth import HTTPTokenAuth
import random, os, string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from sqlalchemy import  Date, func
from datetime import datetime

app=Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "uts.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')
class users(db.Model):
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    token = db.Column(db.String(20), unique=False,nullable=True, primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),default=func.now())
class events(db.Model):
    event_creator = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=True)
    event_start_time = db.Column(Date, unique=False,nullable=False, primary_key=False)
    event_end_time = db.Column(Date, unique=False,nullable=False, primary_key=False)
    event_start_lat= db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_start_lng =db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),default=func.now())
class logs(db.Model):
    username = db.Column(db.String(20), unique=False,nullable=False, primary_key=True)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),default=func.now())
db.create_all()

@app.route('/api/v1/users/create', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = users(username=username,password=password,token= '')
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg" : "registrasi sukses"}), 200

@app.route('/api/v1/users/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    i=15
    user= users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
           token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = i))
           user.token= token
           db.session.commit()
    return jsonify({"msg": "login sukses","token": token,}), 200

@app.route('/api/v1/events/create', methods=['POST'])
def event():
    token =  request.json['token']
    username=users.query.filter_by(token=token).first()
    event_creator = username.username
    event_name = request.json ['event_name']
    event_start_time = str(request.json['event_start_time'])
    event_end_time = str(request.json['event_end_time'])
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']
    
    event_start_time = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S')
    event_end_time = datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S')
    
    eventt = events(event_creator = event_creator, event_name=event_name, event_start_time=event_start_time, event_end_time=event_end_time,event_start_lat=event_start_lat, event_start_lng=event_start_lng, event_finish_lat=event_finish_lat, event_finish_lng=event_finish_lng)
    
    db.session.add(eventt)
    db.session.commit()
    return jsonify({"msg": "Membuat event sukses"}), 200

@app.route('/api/v1/events/log', methods=['POST'])
def log():
    token =  request.json['token']
    username=users.query.filter_by(token=token).first()
    username = username.username
    event_name = request.json ['event_name']
    log_lat = request.json['log_lat']
    log_lng = request.json['log_lng']
    
    log = logs(username = username, event_name=event_name, log_lat=log_lat , log_lng=log_lng)

    db.session.add(log)
    db.session.commit()
    return jsonify({"msg": "sukses mencatat posisi terbaru"}), 200

@app.route('/api/v1/events/logs', methods=['GET'])
def log_status():
    token =  request.json['token']
    event_name = request.json ['event_name']
    event_name= logs.query.filter_by(event_name=event_name).all()
    
    log_status = []

    for loop in event_name:
        dict_logs = {}
        dict_logs.update({"username": loop.username, "event_name": loop.event_name, "log_lat": loop.log_lat, "log_lng": loop.log_lng, "create_at": loop.created_at})
        log_status.append(dict_logs)
    
    return jsonify(log_status)
    
if __name__ == '__main__':
  app.run(debug = True, port=5000)