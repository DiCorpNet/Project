from api.models import LikeDislike
from django.db.models.signals import post_save, pre_delete


def cache_invalidate_activity(sender, instance, **kwargs):
    instance.invalidate_cache()
