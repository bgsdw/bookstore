from bookstore.app.models import Author
from bookstore.app.services.jwt_service import JWTService
from rest_framework import authentication, exceptions


def get_token_header(request):
    auth = authentication.get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'bearer':
        msg = 'No token provided.'
        raise exceptions.AuthenticationFailed(msg)

    if len(auth) == 1:
        msg = 'Invalid bearer header. No credentials provided.'
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid bearer header. Credentials string should not contain spaces.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        token = auth[1].decode()
        return token
    except UnicodeError:
        msg = 'Invalid bearer header. Credentials string should not contain invalid characters.'
        raise exceptions.AuthenticationFailed(msg)

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = get_token_header(request)
        decoded_token = JWTService.decode_token(token)

        if decoded_token['token_type'] == 'refresh':
            raise exceptions.AuthenticationFailed('Token invalid.')

        author_id = decoded_token['Author_ID']
        try:
            author = Author.objects.get(Author_ID=author_id)
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found.')

        return author, None
