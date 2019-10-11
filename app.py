from flask import Flask, render_template, session,request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, disconnect
from threading import Lock
import sqlalchemy as db
from sqlalchemy.pool import StaticPool
import json

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

engine = db.create_engine('sqlite:///socket.sqlite',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool, 
    echo=True
)

connection = engine.connect()
metadata = db.MetaData()
task = db.Table('task', metadata, autoload=True, autoload_with=engine)
status = db.Table('status', metadata, autoload=True, autoload_with=engine)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        # socketio.emit('my_response',
        #               {'data': 'Server generated event', 'count': count},
        #               namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 1) + 1

    query = db.insert(task) 
    values_list = [{
        'text': message['data'], 
        'description': message['data'], 
        'status': 1,
        'id': 1,
    }]
    connection.execute(query, values_list)

    results = connection.execute(db.select([task])).fetchall()
    results = json.dumps([(dict(row.items())) for row in results])

    emit('my_response',
        {
            'data': results, 
            'count': session['receive_count']
        },
        room='100'
    )

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    join_room('100')

    results = connection.execute(db.select([task])).fetchall()
    results = json.dumps([(dict(row.items())) for row in results])

    session['receive_count'] = session.get('receive_count', 1) + 1
    emit('my_response',
        {
            'data': results, 
            'count': session['receive_count']
        },
        room='100'
    )


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1   
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    socketio.run(app, debug=True)
