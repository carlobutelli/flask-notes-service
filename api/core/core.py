#!/usr/bin/env python3
from flask_migrate import Migrate

from .db_manager import get_db


class Core:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        with app.app_context():
            db = get_db()
            db.init_app(app)
            db.create_all()
            Migrate(app, db)
