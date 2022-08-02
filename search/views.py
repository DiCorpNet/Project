from itertools import chain

from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.views import View

from blog.models import Article, Comment
from django.views.generic import ListView

from django.conf import settings

class SearchList(ListView):
    template_name = 'search/search.html'
    paginate_by = settings.PAGINATE

    def get_queryset(self):
        search_article = SearchVector('title', 'content')
        search_comment = SearchVector('content')
        search_comment_query = SearchQuery(self.request.GET['s'])
        search_article_query = SearchQuery(self.request.GET['s'])
        query_search = []
        query_search.append(Article.objects
                            .annotate(search=search_article, rank=SearchRank(search_article, search_article_query))
                            .filter(search=search_article_query).order_by("-rank"))
        query_search.append(Comment.objects
                            .annotate(search=search_comment, rank=SearchRank(search_comment, search_comment_query))
                            .filter(search=search_comment_query))
        final_set = list(chain(*query_search))
        final_set.sort(key=lambda x: x.create_at, reverse=True)
        return final_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchList, self).get_context_data()
        context['s'] = f"?s={self.request.GET['s']}&"
        context['search_get'] = self.request.GET['s']
        context['inf_search'] = len(self.get_queryset())
        return context
