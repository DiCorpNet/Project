from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, ModelBackend


class Backend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            user.last_online = timezone.now()
            user.save(update_fields=['last_online'])
            return user
        except get_user_model().DoesNotExist:
            print('False User')
            return None