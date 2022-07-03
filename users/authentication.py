import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed

def create_access_token(id):
    payload = {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'iat': datetime.datetime.utcnow()
        }
    token = jwt.encode(payload, 'access_secret', algorithm='HS256')
    return token


def refresh_access_token(id):
    payload = {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
    token = jwt.encode(payload, 'refresh_secret', algorithm='HS256')
    return token

def decode_token(type, token):
    try:
        payload = jwt.decode(token, type, algorithms='HS256')
        return payload['user_id']
    except:
        raise AuthenticationFailed('Not Authorised.')