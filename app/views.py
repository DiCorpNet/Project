import re
from urllib.parse import unquote, urlsplit, urlunsplit
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import  check_for_language
from django.conf import settings
from django.views.generic import ListView

from api.models import Notifications


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def lang(request, lang_code):
    next = request.POST.get('next', request.GET.get('next'))

    if (next or not is_ajax(request)) and not url_has_allowed_host_and_scheme(url=next, allowed_hosts=request.get_host()):

        next = request.META.get('HTTP_REFERER')
        if next:
            next = unquote(next)
        if not url_has_allowed_host_and_scheme(url=next, allowed_hosts=request.get_host()):
            next = '/'
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)

    if lang_code and check_for_language(lang_code):

        if next:
            for code_tulpe in settings.LANGUAGES:
                settings_lang_code = '/' + code_tulpe[0]
                parsed = urlsplit(next)
                if parsed.path.startswith(settings_lang_code):
                    path = re.sub('^' + settings_lang_code, '', parsed.path)
                    next = urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
            response = HttpResponseRedirect(next)

        if hasattr(request, 'session'):
            request.session[settings.LANGUAGE_SESSION_KEY] = lang_code
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH
            )

        if request.user.is_authenticated:
            request.user.language = lang_code
            request.user.save(update_fields=['language'])
    return response


class NotificationList(ListView):
    model = Notifications

    def get_queryset(self):
        result = Notifications.objects.all(self.request.user)
        return result



