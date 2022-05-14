from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response.status_code == 403:
        response.status_code = 401
    return response
