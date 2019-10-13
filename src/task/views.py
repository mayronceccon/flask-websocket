from flask import jsonify, request
from flask.views import MethodView
from src.db.session import Session, Engine
from .models import Task


class TaskView(MethodView):
    def options(self):
        return jsonify(['GET', 'POST'])

    def get(self, id=None, page=1):
        if not id:
            results = Task.find_all(page)
            # result = dict(
            #     datas=record_query.items,
            #     total=record_query.total,
            #     current_page=record_query.page,
            #     per_page=record_query.per_page
            # )
            return jsonify([row.serialize for row in results])
        else:
            results = Task.get(id)
            if results is None:
                return jsonify([])
            return jsonify([results.serialize])

    def put(self, id):
        text = request.json.get('text')
        description = request.json.get('description')
        status_id = request.json.get('status_id')

        task = Task.update(
            id,
            text=text,
            description=description,
            status_id=status_id,
        )

        return jsonify([])
