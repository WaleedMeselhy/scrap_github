from flask import Blueprint
from .apis import (get_repo_depends_on, get_repo, get_repo_depends_on_v2,
                   get_repo_v2, add_scrapyjob)

rest_api = Blueprint('rest api', __name__)
# TODO: authentication
rest_api.route('/repo/', methods=('GET', ))(get_repo_depends_on)
rest_api.route('/repo/v2', methods=('GET', ))(get_repo_depends_on_v2)
rest_api.route('/repo/<repo_id>', methods=('GET', ))(get_repo)
rest_api.route('/repo/v2/<repo_id>', methods=('GET', ))(get_repo_v2)
rest_api.route('/scrapyjob/', methods=('POST', ))(add_scrapyjob)
