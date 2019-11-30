from database_core.database.gateway import DBGateway
from database_core.factories import Repo
from database_core.repositories import RepoRepository
from datetime import datetime
from flask import jsonify, request, abort, make_response
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError
from flask import request
repo_repository = RepoRepository()


def get_repo_depends_on():
    try:
        repos_names = request.args.getlist('deps')
        forked = request.args.get('forked', 0)
        stars = request.args.get('stars', 0)
        objs = repo_repository.get_repos_depends_on_repos(
            DBGateway, repos_names, stars, forked)
        return jsonify([obj.to_native() for obj in objs]), 200
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_repo_depends_on_v2():
    try:
        repos_names = request.args.getlist('deps')
        forked = request.args.get('forked', 0)
        stars = request.args.get('stars', 0)
        objs = repo_repository.get_repos_depends_on_repos(DBGateway,
                                                          repos_names,
                                                          stars,
                                                          forked,
                                                          rest=True)
        return jsonify({'repos': [f'/repo/{obj.id}' for obj in objs]}), 200
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_repo(repo_id):
    try:
        obj = repo_repository.get_by_id(DBGateway, repo_id)
        if obj:
            return jsonify(obj.to_native()), 200
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_repo_v2(repo_id):
    try:
        obj = repo_repository.get_by_id(DBGateway, repo_id, rest=True)
        if obj:
            deps = obj.deps
            obj.deps = []
            obj = obj.to_native()
            obj['deps'] = [f'/repo/v2/{dep.id}' for dep in deps]
            return jsonify(obj), 200
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))
