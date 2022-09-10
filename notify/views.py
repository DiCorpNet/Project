import json

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from django.views.generic import ListView

from .models import Notifications


def get_paginated_page(request, objects, number=10):
    current_page = Paginator(objects, number)

    page = request.GET.get('page') if request.method == 'GET' else json.loads(request.body)['page']
    try:
        return current_page.page(page)
    except PageNotAnInteger:
        return current_page.page(1)
    except EmptyPage:
        return current_page.page(current_page.num_pages)


class IndexNotify(View):
    template_name = 'notify/notifications_list.html'

    def get(self, request):
        result = Notifications.objects.all(self.request.user)
        return render(request=request, template_name=self.template_name,
                      context={'object_list': get_paginated_page(request, result)})

    def post(self, request):
        result = Notifications.objects.all(self.request.user)
        return JsonResponse({
            "result": True,
            "articles": render_to_string(
                request=request,
                template_name='notify/include/notify_lists.html',
                context={'object_list': get_paginated_page(request, result)}
            )
        })
