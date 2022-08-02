from django.template import Library

from blog.models import Article

register = Library()

@register.simple_tag(name='popular_article')
def carousel():
    result = Article.objects.all()[:3]
    arrayList = list()
    i = int(0)
    for item in result:
        iterator = {'position': i, 'popular': item}
        arrayList.append(iterator)
        i = i + 1
    return arrayList

