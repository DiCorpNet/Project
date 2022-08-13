from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class NotificationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def all(self, recipient):
        return self.get_queryset().filter(recipient=recipient, read=False)


class Notifications(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    url_to = models.URLField(null=True, blank=True)
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        return f'Уведомление для {self.recipient} | id={self.id}'



