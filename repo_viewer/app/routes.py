from flask import Blueprint
from .apis import charge_balance, create_user, get_all_transactions, get_balance, get_running_pods, get_storage_history

rest_api = Blueprint('rest api', __name__)
# TODO: authentication
rest_api.route('/users/', methods=('POST', ))(create_user)
rest_api.route('/users/<user_id>/', methods=('POST', ))(charge_balance)
rest_api.route('/users/<user_id>/', methods=('GET', ))(get_balance)
rest_api.route('/users/<user_id>/history/',
               methods=('GET', ))(get_all_transactions)
rest_api.route('/users/<user_id>/live/', methods=('GET', ))(get_running_pods)
rest_api.route('/users/<user_id>/storage/',
               methods=('GET', ))(get_storage_history)
