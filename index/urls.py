from django.urls import path

from .views import *


urlpatterns = [
    path('', IndexList.as_view(), name='index_site'),
]