import jwt
from rest_framework import exceptions


class JWTService:
    @classmethod
    def encode_token(self, data):
        return jwt.encode(data, 'K1K0', algorithm='HS256')
    
    @classmethod
    def decode_token(self, token):
        try:
            token = jwt.decode(token, 'K1K0', algorithms=['HS256'])
            return token
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token invalid.')
