from database_core.database.gateway import DBGateway
from database_core.factories import Repo
from database_core.repositories import RepoRepository
from datetime import datetime
from flask import jsonify, request, abort, make_response
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError

repo_repository = PodRepository()



def create_user():
    try:
        usr = User(request.json)
        usr.validate()
        obj = user_repository.create(DBGateway, **usr.to_native())
        return jsonify(obj.to_native()), 201
    except IntegrityError as e:
        abort(make_response(jsonify(message="user already exist"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def charge_balance(user_id):
    try:
        data = request.json
        data.update(user_id=user_id)
        deposit = Deposit(data)
        deposit.validate()
        obj = deposit_repository.create(DBGateway, **deposit.to_native())
        return jsonify(obj.to_native()), 201
    except IntegrityError as e:
        abort(make_response(jsonify(message="integrity error"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_balance(user_id):
    obj = user_repository.get_by_id(DBGateway, ident=user_id)
    if obj is None:
        abort(make_response(jsonify(message="user does not exist"), 404))
    return jsonify(obj.to_native()), 200


def get_running_pods(user_id):
    objs = pod_repository.filter(DBGateway, end_time=None, user_id=user_id)
    return jsonify([obj.to_native() for obj in objs]), 200


def get_storage_history(user_id):
    try:
        # TODO enhance validation
        start_time = datetime.fromtimestamp(
            float(request.args.get('start_time', None)))
        end_time = datetime.fromtimestamp(
            float(request.args.get('end_time', None)))
    except:
        abort(
            make_response(
                jsonify(message="start_time and end_time are required params"),
                400))
    else:
        # TODO: filter by period
        objs = storage_repository.get_storage_in_period(DBGateway,
                                                        user_id=user_id,
                                                        start_time=start_time,
                                                        end_time=end_time)
        return jsonify([obj.to_native() for obj in objs]), 200


def get_all_transactions(user_id):
    try:
        # TODO enhance validation
        start_time = datetime.fromtimestamp(
            float(request.args.get('start_time', None)))
        end_time = datetime.fromtimestamp(
            float(request.args.get('end_time', None)))
    except:
        abort(
            make_response(
                jsonify(message="start_time and end_time are required params"),
                400))
    else:
        pods = pod_repository.get_pods_in_period(DBGateway,
                                                 user_id=user_id,
                                                 start_time=start_time,
                                                 end_time=end_time)
        deposits = deposit_repository.get_deposits_in_period(
            DBGateway,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time)
        user = user_repository.get_by_id(DBGateway, ident=user_id)
        print(f"AAAAAAAA {user}")
        return jsonify({
            'balance': user.balance if user else 0,
            'pods': [pod.to_native() for pod in pods],
            'deposits': [deposit.to_native() for deposit in deposits],
        }), 200
