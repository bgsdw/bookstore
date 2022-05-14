from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        if response.status_code == 403:
            if exc in ['Author not found with this credential.', 'Wrong credential.']:
                response.status_code = 200
            else:
                response.status_code = 401
        elif response.status_code == 404:
            response.status_code = 200
    else:
        response = Response()
        response.data = {'detail': 'Internal server error.'}
    return response
