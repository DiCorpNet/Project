from django.db import models
from django.conf import settings

from blog.models import Article, Comment
from django.db.models.signals import post_save

from .utils import comment_save


class NotificationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def all(self, recipient):
        return self.get_queryset().filter(to_user=recipient, read=False).order_by('-id')


class Notifications(models.Model):
    COMMENT = 'Comment'
    MESSAGE = 'Message'
    ARTICLE = "Article"

    CHOICES = (
        (COMMENT, 'Comment'),
        (MESSAGE, 'Message'),
        (ARTICLE, 'Article')
    )

    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='from_user')
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        return f'Уведомление для {self.to_user} | id={self.id}'


def notify_create_article(instance, **kwargs):
    try:
        Article.objects.get(pk=instance.pk)
        if instance.user.is_superuser:
            text = 'Запись успешно обновлена.'
        else:
            text = 'Запись обновлена успешно.'
    except Article.DoesNotExist:
        if instance.user.is_superuser:
            text = 'Запись Успешно создана. На редактирование есть 15 дней!'
        else:
            text = 'Запись создана успешно. После модерации она появится на сайте.'

    Notifications.objects.create(
        to_user=instance.user, from_user=instance.user,
        text=text,
        article=instance,
        type='Article',
    )


post_save.connect(comment_save, sender=Comment)
post_save.connect(notify_create_article, sender=Article)
