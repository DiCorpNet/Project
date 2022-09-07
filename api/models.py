from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver




