from flask import Flask, render_template, redirect, url_for, request, jsonify, session, send_from_directory
from flask_socketio import SocketIO, join_room
from flask_cors import CORS, cross_origin
from random import randint
import uuid
import tasks
import os


app=Flask(__name__)
app.secret_key="DataRoadReflect"

socketio = SocketIO(app, message_queue='amqp://admin:mypass@rabbit:5672/')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
CORS(app, expose_headers='Authorization')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(root, path)

@app.route("/", methods=['GET'])
def index():
    # create a unique session id

    if 'uid' not in session:
        session['uid']=str(uuid.uuid4())

    return render_template('index.html')


@app.route("/runTask", methods=['POST'])
def long_task():
    file = request.files['file']
    extension='.csv'
    csvName = str(uuid.uuid4()) + extension
    response = jsonify({'filename': csvName})
    csvDirectory = os.path.join(UPLOAD_FOLDER,'csv')
    csvPath = "/".join([csvDirectory, csvName])
    file.save(csvPath)

    n=randint(0,100)
    # if 'uid' not in session:
    #     session['uid']=str(uuid.uuid4())
    sid=str(session['uid'])
    task=tasks.long_task.delay(n=n, session=sid)

    return  jsonify({'id':task.id})

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    extension='.csv'
    csvName = str(uuid.uuid4()) + extension
    response = jsonify({'filename': csvName})
    csvDirectory = os.path.join(UPLOAD_FOLDER,'csv')
    csvPath = "/".join([csvDirectory, csvName])
    file.save(csvPath)

    n=randint(0,100)
    # if 'uid' not in session:
    #     session['uid']=str(uuid.uuid4())
    sid=request.form.get('sid')
    task=tasks.long_task.delay(n=n, path=csvPath, session=sid)

    return  jsonify({'id':task.id})

@socketio.on('connect')
def socket_connect():
    pass

@socketio.on('join_room',namespace='/long_task')
def on_room():
    room=str(session['uid'])
    print('Room: %sy' %(room))
    print('join room {}'.format(room))
    join_room(room)

@socketio.on('join_room_2',namespace='/long_task')
def on_room_2(c):
    room=c['sid']
    print('Room: %s' %(room))
    print('join room {}'.format(room))
    join_room(room)


if __name__=="__main__":
    socketio.run(app,debug=True, host="0.0.0.0")


