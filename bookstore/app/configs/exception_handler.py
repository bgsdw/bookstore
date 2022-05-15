from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        if response.status_code == 403:
            if str(exc) in ['Author not found with this credential.', 'Wrong credential.']:
                response.status_code = 200
            else:
                response.status_code = 401
        elif response.status_code == 404:
            response.status_code = 200
        elif response.status_code == 400:
            # if str(exc) == "{'Email': [ErrorDetail(string='author with this Email already exists.', code='unique')]}":
            #     response.status_code = 200
            # elif 'This field is required.' in str(exc):
            #     response.status_code = 200
            # else:
            response.status_code = 200
            
    else:
        response = Response()
        response.data = {'detail': 'Internal server error.'}
    return response
