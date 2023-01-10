#!/usr/bin/env python3
from flask import Blueprint, request, render_template
from flask_login import current_user, login_required

from api.auth.handler import sign_up, signin, logoff

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route('/sign-up', methods=['GET', 'POST'])
# @swag_from('./api/docs/auth/register.yml')
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        return sign_up(data=data)
    return render_template("sign_up.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
# @swag_from('./api/docs/auth/login.yml')
def login():
    if request.method == 'POST':
        return signin()
    return render_template("login.html", user=current_user)


@auth.route('logout')
# @swag_from('./api/docs/auth/logout.yml')
@login_required
def logout():
    return logoff()
