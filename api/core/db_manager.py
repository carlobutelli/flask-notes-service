#!/usr/bin/env python3
from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_db():
    """Return the db for the app or create it if is needed

    :return: A SQLAlchemy db
    :rtype: SQLAlchemy
    """
    if 'db' not in g:
        g.db = db

    return g.db
