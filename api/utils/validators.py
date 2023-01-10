#!/usr/bin/env python3
import re

import validators
from flask import jsonify, flash, g
from flask_api.status import HTTP_400_BAD_REQUEST

from api.core.logs import log_error_with_txn_id
from api.exceptions import ValidationError


def validate_data_keys(data: dict, keys: set):
    if not data:
        log_error_with_txn_id("[VALIDATION]", g.transaction_id, "payload data not found")
        raise ValidationError("payload not found", list(keys))

    # check if all the data is present
    if not keys.issubset(data.keys()):
        log_error_with_txn_id("[VALIDATION]", g.transaction_id, "incorrect keys in payload")
        raise ValidationError("missing fields",
                              list(keys - set(data.keys())))


def validate_content_keys(data: dict, keys: set):
    if not data:
        log_error_with_txn_id("[VALIDATION]", g.transaction_id, "payload data not found")
        raise ValidationError("data not found", list(keys))

    # check that all keys are not empty
    for key in keys:
        value = data.get(key)
        if value is None or value == "":
            raise ValidationError("field empty", [key])


def validate_email(email: str):
    if not validators.email(email):
        flash('Email not valid.', category='error')
        # return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST


def validate_username(username: str):
    if not username.isalnum() or " " in username:
        flash('Username should be alphanumeric, also no spaces', category='error')
        # return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST


def validate_phone(phone: str):
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    if not re.match(validate_phone_number_pattern, phone):
        flash('Phone number not valid.', category='error')
        return jsonify({'error': "Phone number is not valid"}), HTTP_400_BAD_REQUEST

