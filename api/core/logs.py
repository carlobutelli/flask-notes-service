#!/usr/bin/env python3
from flask import current_app as app


def log_info_with_txn_id(module: str = None, transaction_id: str = None, message: str = None):  # pragma: no cover
    app.logger.info(f"{module} {transaction_id}: {message}")


def log_info(module: str = None, message: str = None):  # pragma: no cover
    app.logger.info(f"{module}: {message}")


def log_error_with_txn_id(module: str = None, transaction_id: str = None, message:str = None):  # pragma: no cover
    app.logger.error(f"{module} {transaction_id}: {message}")


def log_error(module: str = None, message: str = None):  # pragma: no cover
    app.logger.error(f"{module}: {message}")


def log_warn_with_txn_id(module: str = None, transaction_id: str = None, message:str = None):  # pragma: no cover
    app.logger.warn(f"{module} {transaction_id}: {message}")


def log_debug_with_txn_id(module: str = None, transaction_id: str = None, message:str = None):  # pragma: no cover
    app.logger.debug(f"{module} {transaction_id}: {message}")


def log_debug(module: str = None, message: str = None):  # pragma: no cover
    app.logger.debug(f"{module}: {message}")