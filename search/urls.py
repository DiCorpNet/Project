from django.urls import path, re_path

from .views import SearchList


urlpatterns = [
    re_path('^$', SearchList.as_view(), name='search' )
]