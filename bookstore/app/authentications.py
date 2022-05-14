from bookstore.app.models import Author
from rest_framework import authentication, exceptions


def get_token_header(request):
    auth = authentication.get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'bearer':
        return None

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
        author_id = token
        try:
            author = Author.objects.get(Author_ID=author_id)
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found.')

        return author, None
