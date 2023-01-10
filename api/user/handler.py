#!/usr/bin/env python3
from flask import g, request
from flask_api import status
from sqlalchemy.exc import DataError
from sqlalchemy.orm import load_only

from api.core.response import internal_server_error_response, bad_request_response, base_response
from api.user.model import User
from api.core.logs import log_info_with_txn_id, log_error_with_txn_id
from api.exceptions import ValidationError
from api.utils.validators import validate_data_keys, validate_content_keys


def add_user():
    log_info_with_txn_id("[USER]", g.transaction_id, f"request {request.method} {request.path}")
    try:
        data = request.json

        keys = {"email", "password"}
        validate_data_keys(data, keys)
        validate_content_keys(data, keys)

        user = User.deserialize(data, True)
        json_output = {}
        json_output['id'] = user.uuid

        return base_response("CREATED", 201, g.transaction_id, "user created", json_output), status.HTTP_201_CREATED
    except ValidationError as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"refused, payload not valid, {e} Exception TYPE: {type(e)}")
        return bad_request_response()
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def get_users():
    log_info_with_txn_id("[USER]", g.transaction_id, "got new request to get all users")
    try:
        output_fields = ['name', 'phone', 'email', 'created_at', 'updated_at', 'deleted']
        users = User.query.filter(
            User.deleted == False
        ).order_by(
            User.name.asc()
        ).options(
            load_only(*output_fields)
        )

        users_dict = [user.serializer() for user in users]
        return base_response("OK", 200, g.transaction_id, "users retrieved", users_dict), status.HTTP_200_OK
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def get_user(guid: str):
    log_info_with_txn_id("[USER]", g.transaction_id, "got new request to get user by guid")
    try:
        # Get query parameters
        # args = request.args
        # offset = args.get('offset')
        # limit = args.get('limit')
        # print(f"offset: {offset}, limit: {limit}")

        # get in header data
        # request_id = request.headers.get('X-Request-ID')
        # print(f"X-Request-ID: {request_id}")
        #
        # cookie = request.cookies.get("debug")
        # print(f"debug set: {cookie}")

        user = User.query.filter(
            User.uuid == guid
        ).first()

        if not user:
            return base_response("NOT FOUND",
                                 404,
                                 g.transaction_id,
                                 f"no user with guid {guid} found"), status.HTTP_404_NOT_FOUND
        user = user.serializer()

        return base_response("OK", 200, g.transaction_id, "user retrieved", user), status.HTTP_200_OK
    except DataError as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"bad request, {e} Exception TYPE: {type(e)}")
        return bad_request_response()
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def update_user_put(guid: str):
    try:
        user = User.query.filter(
            User.uuid == guid
        ).first()

        if not user:
            return base_response("NOT FOUND",
                                 404,
                                 g.transaction_id,
                                 f"no user with guid {guid} found"), status.HTTP_404_NOT_FOUND
        data = request.json

        user.name = data.get('name')
        user.phone = data.get('phone')
        user.email = data.get('email')
        user.update()

        json_output = {}
        json_output['id'] = guid

        # return make_response(jsonify(status="updated", updated_guid=user.uuid), status.HTTP_200_OK)
        return base_response("OK", 200, g.transaction_id, f"user updated", json_output), status.HTTP_200_OK
    except DataError as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"bad request, {e} Exception TYPE: {type(e)}")
        return bad_request_response()
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"internal server error {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def delete_user(guid: str):
    try:
        user = User.query.filter(
            User.uuid == guid
        ).first()

        if not user:
            return base_response("NOT FOUND",
                                 404,
                                 g.transaction_id,
                                 f"no user with guid {guid} found"), status.HTTP_404_NOT_FOUND
        user.delete()
        json_output = {}
        json_output['id'] = user.uuid

        return base_response("OK",
                             200,
                             g.transaction_id,
                             "user deleted", json_output), status.HTTP_200_OK
    except DataError as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"bad request, {e} Exception TYPE: {type(e)}")
        return bad_request_response()
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id,
                              f"internal server error {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()
