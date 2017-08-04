

import logging
import time
import requests
import json
from threading import Thread
from flask import Flask, request
from database import init_db
from models import User
from database import db_session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
open_boolean = False
init_db()

u = User('admins', 'adminds')
db_session.add(u)
db_session.commit()
q = db_session.query(User)
print q
print q.column_descriptions
for qq in q:
    print qq



def timer():
    count = 0
    print "in timer"
    while True:
        print " sleep"
        global open_boolean
        open_boolean = not open_boolean
        createRequest()
        time.sleep(50)

def createRequest():
    url = 'https://fcm.googleapis.com/fcm/send'
    payload = {'data': {'status': 'test'}, 'to' : 'e5P-SZOXmNY:APA91bEIDqjSB0tmSMS4Pzg1vR7AwlLBQCb_VaeRF_3cgJo63ofgtQXvN-B9MhB6OgtsJyK4_ljSr3OCvME4TFvjDsLEGTYSktsuQ02mWOPlEoDeZOunwgQnN7XH8RB7N9QdXqV8QzzM' }
    headers = {'Content-Type': 'application/json', 'Authorization':'key=AIzaSyBZLyqiF3yY0ksbH8VsSx6U6PCxysHRs74' }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print response.text

@app.route('/register/<id>', methods=['GET'])
def register(id):
    """Return a friendly HTTP greeting."""

    u = User(id, id)
    db_session.add(u)
    db_session.commit()
    return '<h2> register %s </id>' %id

@app.route('/unregister/<id>', methods=['GET'])
def unregister(id):
    return'<h3> unregister %s </h3>' %id

@app.route('/unregister/list', methods=['GET'])
def list():
    users = db.session.query.all()
    for user in users:
        print user.name
    return'<h3> list %s </h3>' %id
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    query = db_session.query(User)
    string = " <html> <body> < ul >"



    for item in query:
        string +=  " < li > "  + item.name   + " < / li > "
    string += " </ul> </body> </html> "
    print string
    return string



if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
db.create_all()
background_thread = Thread(target=timer)
background_thread.start()