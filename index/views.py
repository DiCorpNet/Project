from os.path import split

from django.shortcuts import render

# Create your views here.
from blog.models import Article


# def getIndexSite(request):
#     result = Article.objects.all().prefetch_related('likes', 'user', 'bookmark_article')[:3]
#     return render(request, 'index/index.html', {'object_list':result})
from django.views import View
from django.views.generic import TemplateView, ListView

from api.mixins import NotificationsMixinList, BreadcrumbMixinList



class IndexList(NotificationsMixinList,BreadcrumbMixinList, ListView):
    model = Article
    template_name = 'index/index.html'

    def get_queryset(self):
        return Article.objects.all().prefetch_related('likes', 'user', 'bookmark_article')[:3]

    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data()
        return context
