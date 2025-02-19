from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import datetime

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    db_session = db.getSession(engine)
    msg = json.loads(request.data)
    username = msg['username']
    password = msg['password']
    res = db_session.query(entities.User).filter(entities.User.username == username).filter(entities.User.password == password)
    #dummy validation
    user = res[:]
    if len(user):
        r_msg = {'msg' : 'Welcome!'}
        session['user'] = json.dumps(user[0], cls = connector.AlchemyEncoder)
        json_msg  = json.dumps(r_msg)
        return Response(json_msg, status=200, mimetype="application/json")
    r_msg = {'msg' : 'Ops!'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=401, mimetype="application/json")


#CRUD users
@app.route('/users', methods = ['POST'])
def create_user():
    #c = json.loads(request.data)
    c = json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    r_msg = {'msg':'UserCreated'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')
    message = { 'status': 404, 'message': 'Not Found'}
    return Response(json.dumps(message), status=404, mimetype='application/json')


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c = json.loads(request.form['values'])

    for key in c.keys():
        setattr(user, key, c[key])

    session.add(user)
    session.commit()
    return 'Updated User'


@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"


@app.route('/current', methods = ['GET'])
def current_user():
    user_json = session['user']
    return Response(user_json, status=200, mimetype='application/json')


@app.route('/messages', methods = ['POST'])
def create_message():
    c = json.loads(request.form['values'])
    message = entities.Message(
        content = c['content'],
        user_from_id = c['user_from_id'],
        user_to_id = c['user_to_id']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    r_msg = {'msg':'Your message was created!'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)


@app.route('/messages/<id>', methods = ['GET'])
def get_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')
    message = {'status': 404, 'message': 'Not Found'}
    return Response(json.dumps(message), status=404, mimetype='application/json')


@app.route('/messages', methods = ['GET'])
def get_messages():
    session_message = db.getSession(engine)
    dbResponse = session_message.query(entities.Message)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages/<user_from>/<user_to>', methods = ['GET'])
def get_users_messages(user_from, user_to):
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message).filter(entities.Message.user_from_id == user_from).filter(entities.Message.user_to_id == user_to)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/send_message/<user_from>/<user_to>', methods = ['POST'])
def send_message(user_from, user_to):
    session = db.getSession(engine)
    message = json.loads(request.data)
    content = message['content']
    user_from_id = user_from
    user_to_id = user_to
    add = entities.Message(
        content=content,
        user_from_id=user_from_id,
        user_to_id=user_to_id
    )
    session.add(add)
    session.commit()
    return "sent"



@app.route('/messages', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    
    for key in c.keys():
        setattr(message, key, c[key])
    
    session.add(message)
    session.commit()
    return 'Updated Message'


@app.route('/messages', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(message)
    session.commit()
    return "Your message was deleted"



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
