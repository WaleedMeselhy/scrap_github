from flask import Blueprint
from .apis import get_repo_depends_on, get_repo

rest_api = Blueprint('rest api', __name__)
# TODO: authentication
rest_api.route('/repo/', methods=('GET', ))(get_repo_depends_on)
rest_api.route('/repo/<repo_id>', methods=('GET', ))(get_repo)