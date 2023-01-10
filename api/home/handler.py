import json

from flask import request, g, jsonify
from flask_api.status import HTTP_400_BAD_REQUEST
from flask_login import current_user

from api.core.logs import log_info_with_txn_id, log_error_with_txn_id
from api.core.response import base_error_response, internal_server_error_response
from api.home.model import Note


def add_note():
    log_info_with_txn_id("[HOME]", g.transaction_id, "got new request to add note")
    try:
        data = request.form.to_dict()

        if len(data['note']) < 1:
            return base_error_response(
                'ERROR', HTTP_400_BAD_REQUEST, g.transaction_id, 'Note is too short'
            ), HTTP_400_BAD_REQUEST

        data['user_uuid'] = current_user.uuid
        new_note = Note.deserialize(data, True)
        log_info_with_txn_id(message=f'added note {new_note.id}', module="[NOTE]", transaction_id=g.transaction_id)
    except Exception as e:
        log_error_with_txn_id("[HOME]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()


def delete_note():
    log_info_with_txn_id("[HOME]", g.transaction_id, "got new request to delete note")
    try:
        note = json.loads(request.data)
        note_id = note['note_id']
        note = Note.query.get(note_id)
        if note and note.user_uuid == current_user.uuid:
            note.delete()
        return jsonify({})
    except Exception as e:
        log_error_with_txn_id("[HOME]", g.transaction_id, f"internal server error, {e} Exception TYPE: {type(e)}")
        return internal_server_error_response()
