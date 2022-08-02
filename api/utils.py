from django.utils.safestring import mark_safe

from .models import Notifications


def comment_save(instance, **kwargs):
    if instance.article.user != instance.user:
        if instance.parent:
            if instance.parent.user != instance.user:
                Notifications.objects.create(
                    recipient=instance.parent.user,
                    text=mark_safe(f'На ваш комментарий <strong>{instance.parent.content}</strong> был получен ответ от пользователя {instance.user.username}'),
                    url_to=instance.article.get_absolute_url() + '#comment-' + str(instance.id)
                )
        else:
            Notifications.objects.create(
                recipient=instance.article.user,
                text=mark_safe(f'К записи {instance.article.title} был оставлен комментарий пользователем {instance.user.username}'),
                url_to=instance.article.get_absolute_url() + '#comment-' + str(instance.id)
            )
    else:
        if instance.parent:
            if instance.parent.user != instance.user:
                Notifications.objects.create(
                    recipient=instance.parent.user,
                    text=mark_safe(
                        f'На ваш комментарий <strong>{instance.parent.content}</strong> был получен ответ от пользователя {instance.user.username}'),
                    url_to=instance.article.get_absolute_url() + '#comment-' + str(instance.id)
                )