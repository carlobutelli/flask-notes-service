#!/usr/bin/env python3
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from api.home.handler import add_note, delete_note

home = Blueprint("home", __name__)

@home.route("/", methods=['GET', 'POST'])
@login_required
def homepage():
    if request.method == 'POST':
        add_note()
    return render_template("home.html", user=current_user), 200


@home.route("/delete", methods=['POST',])
def delete():
    return delete_note()
