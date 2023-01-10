#!/usr/bin/env python3
from flasgger import swag_from
from flask import Blueprint, g, request

from api.admin.handler import check_services
from api.core.logs import log_info_with_txn_id

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/healthcheck")
@swag_from("/api/docs/healthcheck.yml")
def healthcheck():
    log_info_with_txn_id("[HEALTH-CHECK]", g.transaction_id, f"request {request.method} {request.path}")
    if request.method == "GET":
        return check_services()
