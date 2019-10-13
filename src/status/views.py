from flask import jsonify
from flask.views import MethodView
from src.db.session import Session, Engine
from .models import Status


class StatusView(MethodView):
    def get(self, id=None, page=1):
        if not id:
            results = Status.find_all(page)
            # result = dict(
            #     datas=record_query.items,
            #     total=record_query.total,
            #     current_page=record_query.page,
            #     per_page=record_query.per_page
            # )
            return jsonify([row.serialize for row in results])
        else:
            return None
