from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='chat_home'),
    path('search-user/<user_name>/', SearchUser),
    path('create-room/', create_dialog),
    path('open-dialog-user/<str:room>/', OpenDialogUser)
]