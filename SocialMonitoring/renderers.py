from urllib import response
from rest_framework import renderers
import json

class ErrorRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        The function takes in data and returns a JSON response, handling errors if necessary.
        
        :param data: The `data` parameter is the data that needs to be rendered into a response. It can
        be any Python object, such as a dictionary or a list, that needs to be converted into a JSON
        string
        :param accepted_media_type: The accepted media type is the type of media that the client is
        willing to accept in the response. It is usually specified in the request headers
        :param renderer_context: The `renderer_context` parameter is a dictionary that contains
        additional information about the rendering context. It can include information such as the
        request, view, and response objects
        :return: a JSON-encoded string.
        """
        response =''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)
        return response