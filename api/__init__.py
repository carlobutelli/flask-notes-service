import os
import sys
import logging
import uuid

from flasgger import Swagger
from flask import Flask, request, g
from flask_cors import CORS
from flask_login import LoginManager

from api.user.model import User
from .config import DevelopmentConfig, LocalConfig, TestingConfig, ProductionConfig
from .core import Core
from .exceptions import WrongConfiguration


def create_app():
    app = Flask(__name__)

    if not os.getenv('APP_SETTINGS'):
        app_settings = f"api.config.DevelopmentConfig"
    else:
        app_settings = f"api.config.{os.getenv('APP_SETTINGS')}Config"
    app.config.from_object(app_settings)

    Core(app)
    CORS(app)

    # registering blueprints
    from .admin.views import admin as admin_bp
    from .user.views import users as users_bp
    from .ping.views import ping as ping_bp
    from .auth.views import auth as auth_bp
    from .home.views import home as home_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(ping_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    # log handler
    log_level = logging.INFO if not app.config.get("DEBUG") else logging.DEBUG
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s "
        "[in %(pathname)s:%(lineno)d]"
    ))

    logging.getLogger("flask_cors").level = logging.DEBUG

    for h in app.logger.handlers:
        app.logger.removeHandler(h)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uuid):
        return User.query.get(uuid)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, template_file="docs/swagger_template.json", config=swagger_config)

    app.logger.info("[WARMUP]: app successfully instantiated")

    @app.before_request
    def set_transaction_id():
        transaction_id = request.headers.get("X-Request-ID")
        g.transaction_id = transaction_id if transaction_id else str(uuid.uuid4().hex)

    return app

# alembic==1.7.6
# apispec==5.2.1
# apispec-webframeworks==0.5.2
# appnope==0.1.3
# asttokens==2.2.1
# attrs==21.4.0
# backcall==0.2.0
# certifi==2022.12.7
# charset-normalizer==2.0.12
# click==8.0.4
# contextlib2==21.6.0
# coverage==5.3
# decorator==5.1.1
# dnspython==2.2.1
# executing==1.2.0
# flasgger==0.9.5
# Flask==2.1.2
# Flask-API==3.0.post1
# Flask-Login==0.6.2
# flask-apispec==0.11.1
# Flask-Cors==3.0.10
# Flask-Migrate==3.1.0
# Flask-SQLAlchemy==2.5.1
# greenlet==2.0.1
# gunicorn==20.0.4
# idna==3.4
# importlib-metadata==4.11.2
# iniconfig==1.1.1
# ipdb==0.13.4
# ipython==8.7.0
# itsdangerous==2.1.0
# jedi==0.18.2
# Jinja2==3.1.2
# jsonschema==4.4.0
# Mako==1.1.6
# MarkupSafe==2.1.1
# marshmallow==3.14.1
# matplotlib-inline==0.1.6
# mistune==2.0.2
# packaging==22.0
# parso==0.8.3
# pexpect==4.8.0
# pickleshare==0.7.5
# pluggy==0.13.1
# prompt-toolkit==3.0.36
# psycopg2-binary==2.9.5
# ptyprocess==0.7.0
# pure-eval==0.2.2
# py==1.11.0
# Pygments==2.13.0
# pyrsistent==0.18.1
# pystache==0.6.0
# pytest==6.1.1
# python-dateutil==2.8.2
# python-dotenv==0.21.0
# python-editor==1.0.4
# PyYAML==6.0
# requests==2.27.1
# schema==0.7.5
# sentry-sdk==1.5.11
# six==1.16.0
# SQLAlchemy==1.4.31
# stack-data==0.6.2
# toml==0.10.2
# traitlets==5.7.1
# urllib3==1.26.9
# validators==0.18.2
# wcwidth==0.2.5
# webargs==8.1.0
# Werkzeug==2.1.2
# zipp==3.7.0