from flask import render_template, jsonify, request
from flask_cors import CORS
from src.app import App
from src.socketio import Socketio
from src.status.views import StatusView
from src.task.views import TaskView

app = App.get_instance()
socketio = Socketio.get_instance()

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


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


# @app.errorhandler(404)
# def page_not_found(error):
#     return jsonify(['OPSSS...'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
