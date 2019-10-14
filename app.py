from flask import render_template, jsonify, request
from src.app import App
from src.socketio import Socketio
from src.status.views import StatusView
from src.task.views import TaskView

app = App.get_instance()
socketio = Socketio.get_instance()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/users/')
def users():
    users = [
        {'id': 1, 'username': 'mayron.ceccon'}
    ]
    return jsonify(users)


status_view = StatusView.as_view('status_view')
app.add_url_rule(
    '/api/status/', view_func=status_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/api/status/<int:id>', view_func=status_view, methods=['GET']
)

task_view = TaskView.as_view('task_view')
app.add_url_rule(
    '/api/tasks/', view_func=task_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/api/tasks/<int:id>', view_func=task_view, methods=['GET', 'PUT']
)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(['OPSSSS 404'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
