from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'message': 'Success',
        }
        if data:
            if 'detail' in data:
                response_data['error_key'] = data['detail']
                response_data['error_message'] = data['detail']
                response_data['error_data'] = data
            else:
                response_data['data'] = data

        return super().render(response_data, accepted_media_type, renderer_context)