from flask import Blueprint
from .apis import get_repo_depends_on

rest_api = Blueprint('rest api', __name__)
# TODO: authentication
rest_api.route('/repo/', methods=('GET', ))(get_repo_depends_on)
