from threading import Lock
from flask_socketio import emit, join_room, disconnect
from flask import session, copy_current_request_context, \
    request
from src.db.session import Session, Engine
from .socketio import Socketio
from src.status.models import Status
from src.task.models import Task
import json

thread = None
thread_lock = Lock()

socketio = Socketio.get_instance()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        # socketio.emit('my_response',
        #               {'data': 'Server generated event', 'count': count},
        #               namespace='/test')


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 1) + 1

    status = Status(name=message['data'])
    Session.get_instance().add(status)
    Session.get_instance().commit()

    results = Status.find_all(Session.get_instance())
    results = json.dumps([row.serialize for row in results])

    emit('my_response', {
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

    results = Status.find_all(Session.get_instance())
    results = json.dumps([row.serialize for row in results])

    session['receive_count'] = session.get('receive_count', 1) + 1
    emit('my_response', {
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
