from django.urls import path

from .views import ProfileAllList, ProfileUser, ProfileUserComments, ProfileUserArticle, ProfileUserFiles


urlpatterns = [
    path('', ProfileAllList.as_view(), name='profile_all_users'),
    path('<slug:user_slug>/', ProfileUser.as_view(), name='profile_user_get'),
    path('<slug:user_slug>/comments/', ProfileUserComments.as_view(), name='profile_user_comments'),
    path('<slug:user_slug>/article/', ProfileUserArticle.as_view(), name='profile_user_article'),
    path('<slug:user_slug>/filemanager/', ProfileUserFiles.as_view(), name='profile_user_file'),
]