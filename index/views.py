from blog.models import Article
from django.views.generic import ListView
from api.mixins import BreadcrumbMixinList


class IndexList(ListView):
    model = Article
    template_name = 'index/index.html'

    def get_queryset(self):
        return Article.objects.all().prefetch_related('likes', 'user', 'bookmark_article')[:3]
