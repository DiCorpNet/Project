from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app.views import lang, NotificationList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('/accounts/', include('allauth.urls')),
    path('/profile/', include('custom_user.urls')),
    path('/', include('index.urls')),
    path('/blog/', include('blog.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('search/', include('search.urls')),
    path('message/', include('message.urls')),
    path('notify/', NotificationList.as_view(), name='notify'),
]

urlpatterns += i18n_patterns(
    path('', include('index.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('custom_user.urls')),
    path('blog/', include('blog.urls')),
    path('message/', include('message.urls')),
)

urlpatterns += [
    path('lang/<lang_code>/', lang, name='lang'),
]

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)