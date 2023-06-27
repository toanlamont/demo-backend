from flask_restful import Resource
from flask import request, session
from datetime import datetime, timedelta
from ..model import metadata


class Plan(Resource):
    def get(self, *args, **kwargs):
        key = request.args.get("key", None)
        user_id = request.args.get("user_id", None)

        if not all([key, user_id]):
            resp = {"status": False, "description": "Hãy nhập đủ thông tin"}
            return resp, 400

        plan = metadata.PLAN.find_one(
            {"key": key, "user_id": user_id},
            {"_id": False})

        if not plan:
            resp = {"status": False, "description": "Không tìm thấy plan"}
            return resp, 404

        resp = {"status": True, "data": plan}
        return resp, 200

    def delete(self, *args, **kwargs):
        key = request.form.get("key", None)
        user_id = request.form.get("user_id", None)

        if not all([key, user_id]):
            resp = {"status": False, "description": "Hãy nhập đủ thông tin"}
            return resp, 400

        plan = metadata.PLAN.delete_one({"key": key, "user_id": user_id})

        if not plan.deleted_count:
            resp = {"status": False, "description": "Không thể xóa plan"}
            return resp, 400

        resp = {"status": True}
        return resp, 200

    def post(self, *args, **kwargs):
        key = request.form.get("key", None)
        user_id = request.form.get("user_id", None)
        plan = request.form.get("plan", None)
        value = request.form.get("value", None)

        if not all([key, user_id, plan, value]):
            resp = {"status": False, "description": "Hãy nhập đủ thông tin"}
            return resp, 400

        if metadata.PLAN.find_one({"key": key, "user_id": user_id}):
            resp = {"status": False, "description": "Thông tin đã tồn tại"}
            return resp, 400

        status = metadata.PLAN.insert_one(
            {"key": key, "user_id": user_id, "plan": plan, "value": value}
        )
        if not status.inserted_id:
            resp = {"status": False, "description": "Không thể thêm plan"}
            return resp, 400

        return {'status': True}, 201

    def put(self, *args, **kwargs):
        key = request.form.get("key", None)
        user_id = request.form.get("user_id", None)
        plan = request.form.get("plan", None)
        value = request.form.get("value", None)

        if not all([key, user_id]) and not any([plan, value]):
            resp = {"status": False, "description": "Hãy nhập đủ thông tin"}
            return resp, 400

        info = {'plan': plan, 'value': value}
        for param in info.keys():
            if info[param] is None:
                info.pop(param)
        status = metadata.PLAN.update_one({'key': key, 'user_id': user_id},
                                          {'$set': info})

        if not status.modified_count:
            resp = {"status": False,
                    "description": "Không thể cập nhật thông tin"}

            return resp, 400

        return {'status': True}, 200


class Bill(Resource):
    def get(self, *args, **kwargs):
        user_id = request.args.get('user_id', None)
        id = request.args.get('id', None)

        if not all([user_id, id]):
            resp = {"status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}
            return resp, 400

        bill = metadata.BILL.find_one({'id': id, 'user_id': user_id},
                                      {'_id': False})
        if not bill:
            resp = {"status": False,
                    "description": "Không tìm thấy thông tin"}
            return resp, 404

        return bill, 200

    def delete(self, *args, **kwargs):
        user_id = request.form.get('user_id', None)
        id = request.form.get('id', None)

        if not all([user_id, id]):
            resp = {"status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}
            return resp, 400

        status = metadata.BILL.delete_one({'id': id, 'user_id': user_id})
        if not status.deleted_count:
            resp = {"status": False,
                    "description": "Không thể xóa mục này"}
            return resp, 404

        return {'status': True}, 200

    def post(self, *args, **kwargs):
        user_id = request.form.get('user_id', None)
        id = request.form.get('id', None)
        money = request.form.get('money', None)
        icon = request.form.get('icon', None)
        type = request.form.get('type', None)
        category = request.form.get('category', None)
        time = request.form.get('time', None)
        note = request.form.get('note', None)

        if not all([user_id, id]):
            resp = {"status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}
            return resp, 400

        try:
            datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        except Exception:
            resp = {"status": False,
                    "description": "Định dạng 'time' không hợp lệ"}

            return resp, 400

        if metadata.BILL.find_one({'user_id': user_id, 'id': id}):
            resp = {"status": False,
                    "description": "Bill id đã tồn tại"}

            return resp, 400

        bill_doc = {
            'user_id': user_id,
            'id': id,
            'money': money,
            'icon': icon,
            'type': type,
            'category': category,
            'time': time,
            'note': note,
        }

        status = metadata.BILL.insert_one(bill_doc)
        if not status.inserted_id:
            resp = {"status": False,
                    "description": "Không thể thêm thông tin"}

            return resp, 400

        resp = {'status': True}

        return resp, 201

    def put(self, *args, **kwargs):
        user_id = request.form.get('user_id', None)
        id = request.form.get('id', None)
        money = request.form.get('money', None)
        icon = request.form.get('icon', None)
        type = request.form.get('type', None)
        category = request.form.get('category', None)
        time = request.form.get('time', None)
        note = request.form.get('note', None)

        if not all([user_id, id]) and not any(
                [money, icon, type, category, time, note]):
            resp = {"status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}
            return resp, 400

        try:
            datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        except Exception:
            resp = {"status": False,
                    "description": "Định dạng 'time' không hợp lệ"}

            return resp, 400

        bill_doc = {
            'money': money,
            'icon': icon,
            'type': type,
            'category': category,
            'time': time,
            'note': note,
        }
        for key in bill_doc.keys():
            if bill_doc[key] is None:
                bill_doc.pop[key]

        status = metadata.BILL.update_one(
            {'id': id, 'user_id': user_id}, {'$set': bill_doc})

        if not status.modified_count:
            resp = {"status": False,
                    "description": "Không thể cập nhật thông tin"}

            return resp, 400

        resp = {'status': True}

        return resp, 200


class BillGet(Resource):
    def get(self, *args, **kwargs):
        user_id = request.args.get('user_id')
        get_type = kwargs.get('type', None)

        if not all([user_id, get_type]):
            resp = {"status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}

            return resp, 400

        if get_type == 'getAll':
            all_bills = list(metadata.BILL.find(
                {'user_id': user_id}, {'_id': False}))
            return {'status': True, 'data': all_bills}, 200

        elif get_type == 'inWeek':
            date = datetime.utcnow() + timedelta(hours=7)
            start_week = (date - timedelta(days=date.weekday())).date()
            end_week = start_week + timedelta(days=7)
            start_week_query = datetime.strftime(
                start_week, '%Y-%m-%dT%H:%M:%SZ')
            end_week_query = datetime.strftime(
                end_week, '%Y-%m-%dT%H:%M:%SZ')
            in_week_bills = list(metadata.BILL.find({
                'user_id': user_id,
                'time': {
                    '$lt': end_week_query,
                    '$gte': start_week_query
                }}, {'_id': False}))
            return {'status': True, 'data': in_week_bills}, 200

        elif get_type == 'lastWeek':
            date = datetime.utcnow() + timedelta(hours=7) - timedelta(days=7)
            start_last_week = (date - timedelta(days=date.weekday())).date()
            end_last_week = start_week + timedelta(days=7)
            start_week_query = datetime.strftime(
                start_last_week, '%Y-%m-%dT%H:%M:%SZ')
            end_week_query = datetime.strftime(
                end_last_week, '%Y-%m-%dT%H:%M:%SZ')
            in_week_bills = list(metadata.BILL.find({
                'user_id': user_id,
                'time': {
                    '$lt': end_week_query,
                    '$gte': start_week_query
                }}, {'_id': False}))
            return {'status': True, 'data': in_week_bills}, 200

        elif get_type == 'byDay':
            day = request.args.get('day', '')
            if not day:
                resp = {"status": False,
                        "description": "Hãy nhập đầy đủ thông tin"}

                return resp, 400

            try:
                date = datetime.strptime(day, '%d-%m-%Y')
            except Exception:
                resp = {"status": False,
                        "description": "Định dạng ngày không hợp lệ"}
                return resp, 400

            start_day_query = datetime.strftime(date, '%Y-%m-%dT%H:%M:%SZ')
            end_day_query = datetime.strftime(
                (date + timedelta(days=1)), '%Y-%m-%dT%H:%M:%SZ')

            by_day_bills = list(metadata.BILL.find({
                'user_id': user_id,
                'time': {
                    '$lt': end_day_query,
                    '$gte': start_day_query
                }}, {'_id': False}))

            return {'status': True, 'data': by_day_bills}, 200

        elif get_type == 'byMonth':
            month = request.args.get('month', '')
            if not day:
                resp = {"status": False,
                        "description": "Hãy nhập đầy đủ thông tin"}
                return resp, 400

            if not month.isdigit() or int(month) not in range(1, 13):
                resp = {"status": False,
                        "description": "Định dạng tháng không hợp lệ"}
                return resp, 400

            start_month = datetime(datetime.now().year, int(month), 1)
            end_month = (
                datetime(datetime.now().year, int(month), 28) + timedelta(
                    days=4)).replace(day=1)
            start_month_query = datetime.strftime(
                start_month, '%Y-%m-%dT%H:%M:%SZ')
            end_month_query = datetime.strftime(
                end_month, '%Y-%m-%dT%H:%M:%SZ')

            by_month_bills = list(metadata.BILL.find({
                'user_id': user_id,
                'time': {
                    '$lt': end_month_query,
                    '$gte': start_month_query
                }}, {'_id': False}))

            return {'status': True, 'data': by_month_bills}, 200


class User(Resource):
    def get(self, *args, **kwargs):
        user_id = request.args.get('user_id', None)

        if not user_id:
            resp = {
                "status": False,
                "description": "Hãy nhập đầy đủ thông tin"}

            return resp, 400

        user_doc = metadata.USER.find_one({'user_id': user_id}, {'_id': False})

        if not user_doc:
            resp = {
                "status": False,
                "description": "Không tìm thấy user"}

            return resp, 404

        resp = {'status': True, 'data': user_doc}
        return resp, 200

    def post(self, *args, **kwargs):
        username = request.form.get('username', None)
        user_id = request.form.get('user_id', None)
        password = request.form.get('password', None)
        if not all([username, user_id, password]):
            resp = {
                "status": False,
                "description": "Hãy nhập đầy đủ thông tin"}

            return resp, 400

        if metadata.USER.find_one({'$or': [
            {'username': username},
            {'user_id': user_id}
        ]}):
            resp = {
                "status": False,
                "description": "Thông tin đã tồn tại"}

            return resp, 400

        user_doc = {
            'username': username,
            'user_id': user_id,
            'password': password
        }

        status = metadata.USER.insert_one(user_doc)
        if not status.inserted_id:
            resp = {
                "status": False,
                "description": "Không thể thêm tài khoản"}

            return resp, 400

        resp = {'status': True}

        return resp, 200


class UserAction(Resource):
    def post(self, **kwargs):
        action = kwargs.get('action', None)

        if action == 'login':
            username = request.form.get('username', None)
            password = request.form.get('password', None)

            if not all([username, password]):
                resp = {
                    "status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}

                return resp, 400

            user_doc = metadata.USER.find_one({
                'username': username,
                'password': password
                }, {'_id': False})
            if not user_doc:
                resp = {
                    "status": False,
                    "description": "Thông tin tài khoản không chính xác"}

                return resp, 400

            resp = user_doc

            return resp, 200

        elif action == 'logout':
            user_id = request.form.get('user_id', None)
            if not user_id:
                resp = {
                    "status": False,
                    "description": "Hãy nhập đầy đủ thông tin"}

                return resp, 400

            user_doc = metadata.USER.find_one({
                'user_id': user_id
                })
            if not user_doc:
                resp = {
                    "status": False,
                    "description": "Không tìm thấy user_id"}

                return resp, 400

            session.clear()

            resp = {'status': True}

            return resp, 200

