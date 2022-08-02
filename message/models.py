from django.conf import settings
from django.db import models

# Create your models here.


class MessageRoom(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dialog_layer')
    layer = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.layer


class MessageDialog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layer = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text