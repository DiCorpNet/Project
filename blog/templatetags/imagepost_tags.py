from django.template import Library
from django.templatetags.static import static

register = Library()

@register.filter()
def image_post(image):
    if not image:
        return static('images/small/small-3.jpg')
    return image.url