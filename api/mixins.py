from django import views
from app.models import Category
from blog.models import Article


class BreadcrumbMixinList(views.generic.list.MultipleObjectMixin):

    @staticmethod
    def breadcrumb(url):
        strip_l = url.lstrip('/en/').lstrip('/ru/')
        strip_r = strip_l.rstrip('/')
        st = strip_r.split('/')
        result = []
        if len(st) != 0:
            i = 1
            for item in st:
                if Category.objects.filter(slug=item).exists():
                    dicts = Category.objects.get(slug=item)
                    if len(st) == i:
                        data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': True}
                        result.append(data)
                        i = i + 1
                    else:
                        data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': False}
                        result.append(data)
                        i = i + 1
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['breadcrumbs'] = self.breadcrumb(self.request.get_full_path())
        return context


class BreadcrumbMixinDetail(views.generic.detail.SingleObjectMixin):

    @staticmethod
    def breadcrumb(url):
        strip_l = url.lstrip('/en/').lstrip('/ru/')
        strip_r = strip_l.rstrip('/')
        st = strip_r.split('/')
        result = []
        if len(st) != 0:
            i = 1
            for item in st:
                if Category.objects.filter(slug=item).exists():
                    dicts = Category.objects.get(slug=item)
                    if len(st) == i:
                        data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': True}
                        result.append(data)
                        i = i + 1
                    else:
                        data = {'title': dicts.name, 'url': dicts.get_absolute_url(), 'link': False}
                        result.append(data)
                        i = i + 1
                else:
                    res = Article.objects.get(slug=item)
                    data = {'title':res.title, 'url':res.slug, 'link': True}
                    result.append(data)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['breadcrumbs'] = self.breadcrumb(self.request.get_full_path())
        return context

