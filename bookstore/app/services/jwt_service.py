import jwt
from rest_framework import exceptions
from django.conf import settings


class JWTService:
    @classmethod
    def encode_token(self, data, is_access_token=True):
        return jwt.encode(data, settings.ACCESS_SEC_KEY if is_access_token else settings.REFRESH_SEC_KEY, algorithm='HS256')
    
    @classmethod
    def decode_token(self, token, is_access_token=True):
        try:
            token = jwt.decode(token, settings.ACCESS_SEC_KEY if is_access_token else settings.REFRESH_SEC_KEY, algorithms=['HS256'])
            return token
        except jwt.ExpiredSignatureError:
            msg = 'Token expired.' if is_access_token else 'Refresh token expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Token invalid.' if is_access_token else 'Refresh token invalid.'
            raise exceptions.AuthenticationFailed(msg)
