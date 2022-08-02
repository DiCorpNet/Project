from django.urls import re_path, path

from .consumers import *

websocket_urlpatterns = [
    path('ws/<str:room>/', MessageConsumer.as_asgi())
]