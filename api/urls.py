from django.contrib.auth.decorators import login_required
from django.urls import re_path, path
from .views import add_comment, BlogLike, CommentLike, Bookmark, ApiSearch


urlpatterns = [
    re_path(r'^comment/(?P<article_id>\d+)/', add_comment, name='add_comment'),
    path('bookmark/<pk>/article/', login_required(Bookmark), name='article_bookmark'),
    path('likes/<pk>/article/', login_required(BlogLike)),
    path('likes/<pk>/comment/', login_required(CommentLike)),
    path('search/', ApiSearch, name='api_search')
]