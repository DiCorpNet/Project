import os.path
from pathlib import Path

from django.template import Library
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = Library()

@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False

@register.filter
def urer_true(obj, user):
    if user.is_authenticated:
        return obj.filter(id=user.id).exists()
    return False


@register.filter
def path_file(file):
    excension = os.path.splitext(file.filename())[1].strip('.')
    if excension == 'jpg':
        result = mark_safe(f'<img src="{file.file.url}" class="avatar-sm rounded" alt="file-image" />')
    elif excension == 'jpeg':
        result = mark_safe(f'<img src="{file.file.url}" class="avatar-sm rounded" alt="file-image" />')
    elif excension == 'png':
        result = mark_safe(f'<img src="{file.file.url}" class="avatar-sm rounded" alt="file-image" />')
    elif excension == 'gif':
        result = mark_safe(f'<img src="{file.file.url}" class="avatar-sm rounded" alt="file-image" />')
    elif excension == 'webp':
        result = mark_safe(f'<img src="{file.file.url}" class="avatar-sm rounded" alt="file-image" />')
    else:
        result = mark_safe(f'<div class="avatar-sm"><span class="avatar-title rounded">.{excension}</span></div>')

    return result