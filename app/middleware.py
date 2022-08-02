from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LocalMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        if not user:
            return response

        if not user.is_authenticated:
            return response

        user_language = getattr(user, 'language', None)
        if not user_language:
            return response

        next_trans = translate_url(request.path, user_language)
        if next_trans != request.path:
            translation.activate(user_language)
            response = HttpResponseRedirect(next_trans)
        return response