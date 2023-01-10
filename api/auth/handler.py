#!/usr/bin/env python3
from flask import request, g, redirect, url_for
from flask_api.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from api.core.logs import log_error_with_txn_id, log_info_with_txn_id
from api.core.response import bad_request_response, internal_server_error_response, base_error_response
from api.exceptions import ValidationError
from api.user.model import User
from api.utils.validators import validate_data_keys, validate_content_keys, validate_email, validate_phone


def sign_up(data: dict):
    try:
        keys = {"name", "phone", "email", "password", "password2"}
        validate_data_keys(data, keys)
        validate_content_keys(data, keys)
        validate_email(data['email'])
        validate_phone(data['phone'])

        password = data['password']

        user = User.query.filter_by(email=data['email']).first()

        if user:
            return base_error_response(
                'ERROR', HTTP_409_CONFLICT, g.transaction_id, 'Email is already taken'
            ), HTTP_409_CONFLICT
        elif len(data['name']) < 2:
            return base_error_response(
                'ERROR', HTTP_400_BAD_REQUEST, g.transaction_id, 'First name must be greater than 1 character'
            ), HTTP_400_BAD_REQUEST
        elif len(password) < 6:
            return base_error_response(
                'ERROR', HTTP_400_BAD_REQUEST, g.transaction_id, 'Password is too short (at least 7 characters)'
            ), HTTP_400_BAD_REQUEST
        elif password != data['password2']:
            return base_error_response(
                'ERROR', HTTP_409_CONFLICT, g.transaction_id, 'Passwords don\'t match'
            ), HTTP_409_CONFLICT
        else:
            pwd_hash = generate_password_hash(password, method='sha256')
            data['password'] = pwd_hash
            data.pop('password2')

            user = User.deserialize(data, True)

            login_user(user, remember=True)
            log_info_with_txn_id(message='Account created', module="[AUTH]", transaction_id=g.transaction_id)

            # json_output = { 'user': { 'id': user.uuid, 'name': user.name, "email": user.email } }
            # return base_response("CREATED", 201, g.transaction_id, "user created", json_output), HTTP_201_CREATED
            return redirect(url_for('home.homepage'))
    except ValidationError as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"refused, payload not valid, {e} Exception TYPE: {type(e)}")
        return bad_request_response()
    except Exception as e:
        log_error_with_txn_id("[USER]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def signin():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            # return base_response("OK", 200, g.transaction_id, "user logged in", user.serializer()), HTTP_201_CREATED
            return redirect(url_for('home.homepage'))
        else:
            # return base_error_response(
            #     'ERROR', HTTP_400_BAD_REQUEST, g.transaction_id, 'Incorrect password, try again'
            # ), HTTP_400_BAD_REQUEST
            return redirect(url_for('auth.login'))
    else:
        # return base_error_response(
        #     'ERROR', HTTP_400_BAD_REQUEST, g.transaction_id, 'Email does not exist'
        # ), HTTP_400_BAD_REQUEST
        return redirect(url_for('auth.login'))


def logoff():
    logout_user()
    return redirect(url_for('auth.login'))
