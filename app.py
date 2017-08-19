

import logging
import os
import threading
import time
import datetime
import requests
import json
import sched, time
from threading import Thread
from flask import Flask, request
import sys
from database import init_db
from models import User
from database import db_session
app = Flask(__name__)
open_boolean = False
init_db()
q = db_session.query(User)
print q
print q.column_descriptions
for qq in q:
    print qq


def do_something():
    printToFile("preforming task")
    check_bridge_status()
    threading.Timer(60.0, do_something).start()


def check_bridge_status():
    url = "http://data.goteborg.se/BridgeService/v1.0/GetGABOpenedStatus/f459f514-8dfe-4279-b546-d7a0fb76870c?format=json"
    response = requests.get(url)
    global open_boolean
    json_data = json.loads(response.text)

    printToFile("Bridge status: %s" %json_data)
    if "True" in json_data or "true" in json_data:
        global open_boolean
        open_bridge = True
        bridge_open()
    else:
        global open_boolean
        open_bridge = False
    print json_data

def bridge_open():
    printToFile("open bridge")
    query = db_session.query(User)
    for item in query:
        send_push(item.pushId, 'open')


 #e5P-SZOXmNY:APA91bEIDqjSB0tmSMS4Pzg1vR7AwlLBQCb_VaeRF_3cgJo63ofgtQXvN-B9MhB6OgtsJyK4_ljSr3OCvME4TFvjDsLEGTYSktsuQ02mWOPlEoDeZOunwgQnN7XH8RB7N9QdXqV8QzzM

def send_push(pushId, status):
    url = 'https://fcm.googleapis.com/fcm/send'
    payload = {'data': {'status': status}, 'notification': {'title': 'Gotaalvbron', 'body': status},
               'to': pushId}
    headers = {'Content-Type': 'application/json',
               'Authorization': 'key=AAAABZijzVo:APA91bFX6dsZB6xHpdUZ-SxvXtXPftZ03lQwG1SHYF6R9-27gXxcJhWMtsY6YH0XBAeTfoet03x71ZzA15m9fsbmTGW2V30KflP8LjX3LrdAC-zeBWilnXNN01nUJzQDKnPRrCIHLRPK'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print response.text

def bridge_closed():
    query = db_session.query(User)
    for item in query:
        send_push(item.pushId, 'closed')

@app.route('/register/', methods=['GET'])
def register():
    """Return a friendly HTTP greeting."""
    pushId = request.args.get('pushId')
    pushType = request.args.get('pushType')
    pushBridype = request.args.get('bridgeType')
    u = User(pushId=pushId, pushType=pushType, bridgeType=pushBridype)
    db_session.add(u)
    db_session.commit()
    printDBLog()
    return '<h2> register %s </id>' %pushId

@app.route('/unregister/', methods=['GET'])
def unregister():
    pushId = request.args.get('pushId')
    pushBridype = request.args.get('bridgeType')
    User.query.filter_by(pushId=pushId).delete()
    db_session.commit()
    printDBLog()
    return '<h2> unregister %s </id>' %pushId

@app.route('/openbridge/', methods=['GET'])
def openbridge():
    bridge_open()
    return '<h2> open </id>'

@app.route('/status/', methods=['GET'])
def status():
    bridgeType = request.args.get('bridgeType')
    global open_boolean
    data = {}
    data[bridgeType] = open_boolean
    json_data = json.dumps(data)
    return json.dumps(data)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    query = db_session.query(User)
    string = ""
    for item in query:
        string += str(item) + '\n'
    print string
    return string

def printDBLog():
    query = db_session.query(User)
    string = ""
    for item in query:
        string += str(item) + '\n'
    print string


def printToFile(text):
    print text
    filename = 'log.txt'

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    logfile = open(filename,append_write)
    logfile.write(str(datetime.datetime.now().time()) + ' ' + text + '\n')
    logfile.close()

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    print "111"
    do_something()
    app.run(host='127.0.0.1', port=8080, debug=True)
    print  "222"
