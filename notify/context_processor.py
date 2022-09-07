from app.models import Category
from blog.models import Article


def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.filter(read=False).order_by('-id')}
    else:
        return {'notifications': []}


# def breadcrumb(request):
#     strip_l = request.get_full_path().lstrip('/en/').lstrip('/ru/')
#     strip_r = strip_l.rstrip('/')
#     st = strip_r.split('/')
#     print(st)
#     result = []
#     print(len(st))
#     if len(st) != 1:
#         i = 1
#         for item in st:
#             if Category.objects.filter(slug=item).exists():
#                 dicts = Category.objects.get(slug=item)
#                 if len(st) == i:
#                     data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': True}
#                     result.append(data)
#                     i = i + 1
#                 else:
#                     data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': False}
#                     result.append(data)
#                     i = i + 1
#             else:
#                 print('Article')
#                 res = Article.objects.get(slug=item)
#                 data = {'title':res.title, 'url':res.slug, 'link': True}
#                 result.append(data)
#     return {'breadcrumbs': result}