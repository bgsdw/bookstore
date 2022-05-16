from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'message': 'Success',
        }
        if data:
            if 'detail' in data:
                error_key = 'error_internal_server'
                if data['detail'] == 'Token expired.':
                    error_key = 'error_expired_token'
                elif data['detail'] == 'Refresh token expired.':
                    error_key = 'error_refresh_token_expired'
                elif data['detail'] == 'Token invalid.' or data['detail'].startswith('Invalid bearer header.'):
                    error_key = 'error_invalid_token'
                elif data['detail'] == 'Refresh token invalid.':
                    error_key = 'error_refresh_token_invalid'
                elif data['detail'] == 'No token provided.':
                    error_key = 'error_no_auth_token'
                elif data['detail'] == 'Author not found with this credential.':
                    error_key = 'error_email_not_found'
                elif data['detail'] == 'Wrong credential.':
                    error_key = 'error_invalid_password'
                elif data['detail'] == 'Internal server error.':
                    error_key = 'error_internal_server'
                elif data['detail'] == 'Not found.':
                    error_key = 'error_id_not_found'
                response_data['message'] = 'Failed'
                response_data['error_key'] = error_key if error_key else data['detail']
                response_data['error_message'] = data['detail']
                response_data['error_data'] = data
            elif 'Email' in data and 'Error' in str(data['Email']):
                error_key = 'error_internal_server'
                if str(data['Email']) == "[ErrorDetail(string='author with this Email already exists.', code='unique')]":
                    error_key = 'error_email_duplicate'
                response_data['message'] = 'Failed'
                response_data['error_key'] = error_key if error_key else data['Email'][0]
                response_data['error_message'] = data['Email'][0]
                response_data['error_data'] = data
            elif 'This field is required.' in str(data):
                response_data['message'] = 'Failed'
                response_data['error_key'] = 'error_internal_server'
                response_data['error_message'] = 'Some fields are missing.'
                response_data['error_data'] = data
            elif 'object does not exist.' in str(data):
                response_data['message'] = 'Failed'
                response_data['error_key'] = 'error_internal_server'
                response_data['error_message'] = 'Some objects are not exist.'
                response_data['error_data'] = data
            elif 'That choice is not one of the available choices.' in str(data):
                response_data['message'] = 'Failed'
                response_data['error_key'] = 'error_internal_server'
                response_data['error_message'] = 'Some filter keywords are not valid.'
                response_data['error_data'] = data
            else:
                response_data['data'] = data

        return super().render(response_data, accepted_media_type, renderer_context)