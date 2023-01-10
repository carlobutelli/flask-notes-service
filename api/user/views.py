#!/usr/bin/env python3
from flasgger import swag_from
from flask import request, Blueprint

from api.user.handler import add_user, get_users, get_user, update_user_put, delete_user

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("", methods=['POST', 'GET'])
@swag_from('/api/docs/add_user.yml', methods=['POST'])
@swag_from('/api/docs/get_users.yml', methods=['GET'])
def user_route():
    if request.method == 'POST':
        return add_user()
    elif request.method == 'GET':
        return get_users()


@users.route("/<string:guid>", methods=('PATCH', 'PUT', 'GET'))
@swag_from("/api/docs/get_user.yml", methods=['GET'])
@swag_from("/api/docs/put_user.yml", methods=['PUT'])
def update_user(guid):
    if request.method == 'GET':
        return get_user(guid=guid)
    elif request.method == 'PUT':
        return update_user_put(guid=guid)
    elif request.method == 'DELETE':
        return delete_user(guid=guid)
