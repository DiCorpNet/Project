from django.template import Library
from django.templatetags.static import static

register = Library()

@register.filter()
def image(img):
    if not img:
        return static('images/users/avatar-2.jpg')
    return img.url