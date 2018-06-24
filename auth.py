import uuid
import tornado.web


class AuthHandler(object):
    def create_token(self):
        return str(uuid.uuid4())

