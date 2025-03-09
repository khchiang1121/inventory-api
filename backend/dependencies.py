import os
from ninja import Schema
from ninja.security import HttpBearer
from ninja.errors import HttpError

class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == os.environ.get("DJANGO_API_TOKEN"):
            return token
        raise HttpError(401, "Invalid or missing API token")

api_auth = TokenAuth()
