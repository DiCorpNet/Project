from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *


urlpatterns = [
    path('', BlogList.as_view(), name='article_list'),
    path('<slug:cat_slug>/', BlogCategoryList.as_view(), name='category_list'),
    path('<slug:category_slug>/<slug:article_slug>/', BlogDetail.as_view(), name='article_detail'),
    path('create-post', login_required(BlogCreatePost.as_view()), name='create-post'),
    path('post/<slug:slug>/edit', login_required(EditArticles.as_view()), name='article-edit'),
    path('post/<slug:slug>/delete', login_required(DeleteArticle.as_view()), name='article-delete')
]