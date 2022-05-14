import jwt
from rest_framework import exceptions


class JWTService:
    @classmethod
    def encode_token(self, data):
        return jwt.encode(data, 'K1K0', algorithm='HS256')
    
    @classmethod
    def decode_token(self, token, is_access_token=True):
        try:
            token = jwt.decode(token, 'K1K0', algorithms=['HS256'])
            return token
        except jwt.ExpiredSignatureError:
            msg = 'Token expired.' if is_access_token else 'Refresh token expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Token invalid.' if is_access_token else 'Refresh token invalid.'
            raise exceptions.AuthenticationFailed(msg)
