from django.views import View

from .models import Category

def category(request):
    result = Category.objects.filter(published=True)
    return {'category_list': result}

class CategoryList(View):

    def category(self):
        result = Category.objects.filter(published=True)
        return {'category_list': result}