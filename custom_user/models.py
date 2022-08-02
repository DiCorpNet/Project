import uuid
from datetime import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from blog.fields import WEBPField
from app.models import Country, Location

# Create your models here.

def upload_avatar(self,filename):
    return 'images/avatar/user_{0}/{1}'.format(self.id, uuid.uuid4().hex)


class User(AbstractUser):
    last_online = models.DateTimeField(null=True, blank=True)
    about_us = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    image = WEBPField(verbose_name='User Avatar', upload_to=upload_avatar, blank=True, null=True)
    link_github = models.URLField(max_length=200, null=True, blank=True)
    link_skype = models.URLField(max_length=200, null=True, blank=True)
    link_vk = models.URLField(max_length=200, null=True, blank=True)

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False

    def get_online_info(self):
        if self.is_online():
            return 'Online'
        if self.last_online:
            return _('Last visit {0}').format(naturaltime(self.last_online))
        return 'Unknown'
