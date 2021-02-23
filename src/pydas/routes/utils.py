from functools import wraps
from flask import request, jsonify, current_app

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)


def validate_token(token):
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    return uid


def get_roles(uid):
    db = firestore.client()
    groups = db.collection(u'groups')
    group_docs = groups.where(u'users', u'array_contains', uid).stream()
    roles = []
    for group in group_docs:
        roles.extend(group.to_dict()['roles'])
    return roles


def verify_scopes(scopes):
    def check_access(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if current_app.config["TESTING"]:
                return fn(*args, **kwargs)

            try:
                token = request.headers.get('Authorization').split()[1]
                uid = validate_token(token)
            except Exception:
                return jsonify(msg='Bad authorization header'), 401
            roles = get_roles(uid)
            if scopes[request.method] not in roles:
                return jsonify(msg='Unauthorized access'), 403
            return fn(*args, **kwargs)
        return wrapper
    return check_access
