from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'message': 'Success',
        }
        if data:
            if 'detail' in data:
                error_key = None
                if data['detail'] == 'Token expired.':
                    error_key = 'error_expired_token'
                elif data['detail'] == 'Token invalid.' or data['detail'].startswith('Invalid bearer header.'):
                    error_key = 'error_invalid_token'
                elif data['detail'] == 'No token provided.':
                    error_key = 'error_no_auth_token'
                response_data['error_key'] = error_key if error_key else data['detail']
                response_data['error_message'] = data['detail']
                response_data['error_data'] = data
            else:
                response_data['data'] = data

        return super().render(response_data, accepted_media_type, renderer_context)