import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from pydas_auth.clients.base import BaseAuthClient


class GoogleFirestoreAuthClient(BaseAuthClient):
    """
    Authentication client implementation for working with Google's Firestore API.
    """

    def __init__(self, config):
        try:
            firebase_admin.get_app()
        except ValueError:
            credential = credentials.Certificate(config)
            firebase_admin.initialize_app(credential)

    @ classmethod
    def can_handle(cls, auth_type):
        return auth_type == 'firestore'

    def validate_token(self, token):
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid

    def get_roles(self, uid):
        database = firestore.client()
        groups = database.collection(u'groups')
        group_docs = groups.where(u'users', u'array_contains', uid).stream()
        roles = []
        for group in group_docs:
            roles.extend(group.to_dict()['roles'])
        return roles
