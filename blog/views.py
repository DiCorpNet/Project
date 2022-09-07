import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView, TemplateView
from django.views.generic.edit import BaseDeleteView

from .forms import CreateFormPost, FilesCreateForm, ArticleEditForm
from .models import Article, Comment, Files
from app.models import Category

from api.forms import CommentForm

from api.mixins import BreadcrumbMixinList, BreadcrumbMixinDetail

def get_paginated_page(request, objects, number=settings.PAGINATE):
    current_page = Paginator(objects, number)

    page = request.GET.get('page') if request.method == 'GET' else json.loads(request.body)['page']
    try:
        return current_page.page(page)
    except PageNotAnInteger:
        return current_page.page(1)
    except EmptyPage:
        return current_page.page(current_page.num_pages)


class BlogList(TemplateView, BreadcrumbMixinList):
    template_name = 'blog/article_list.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={'article_list': get_paginated_page(request, Article.objects.all())})

    def post(self, request):
        return JsonResponse({
            "result": True,
            "articles": render_to_string(
                request=request,
                template_name='blog/modules/article_previews_list.html',
                context={'article_list': get_paginated_page(request, Article.objects.all())}
            )
            })



class BlogDetail(DetailView):
    model = Article
    slug_url_kwarg = 'article_slug'

    def get_queryset(self):
        category = self.kwargs.get('category_slug', '')
        q = Article.objects.filter(slug=self.kwargs.get('article_slug')).select_related('category').prefetch_related('comments')
        return q.filter(category__slug=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_comment'] = CommentForm()
        context['likes_user'] = context['article'].likes.filter(id=self.request.user.id).exists()
        context['files'] = Files.objects.filter(article=context['article'].id)
        context['comments'] = Comment.objects.filter(article_id=context['article'].id).prefetch_related('user', 'parent', "parent__user")
        return context


class BlogCategoryList(View):
    template_name = 'blog/article_list.html'

    def get(self, request, cat_slug):
        result = Article.objects.filter(category__slug=cat_slug).select_related('category').prefetch_related('user', 'comments', 'bookmark_article').order_by('-id')
        return render(request=request, template_name=self.template_name,
                      context={'article_list': get_paginated_page(request, result)})

    def post(self, request, cat_slug):
        result = Article.objects.filter(category__slug=cat_slug).select_related('category').prefetch_related('user', 'comments', 'bookmark_article').order_by('-id')
        return JsonResponse({
            "result": True,
            "articles": render_to_string(
                request=request,
                template_name='blog/modules/article_previews_list.html',
                context={'article_list': get_paginated_page(request, result), 'title': Category.objects.get(slug=cat_slug).name}
            )
            })




class BlogCreatePost(PermissionRequiredMixin, View):
    permission_required = 'blog.add_article'
    template_name = 'blog/create-post.html'

    def get(self, request):
        form = CreateFormPost
        file = FilesCreateForm
        return render(request, self.template_name, {'form': form, 'formfile': file})

    def post(self, *args, **kwargs):
        form = CreateFormPost(self.request.POST or None, self.request.FILES or None)

        if form.is_valid():
            print('Valid')
            obj = form.save(commit=False)
            obj.user = self.request.user
            if self.request.user.is_superuser:
                obj.is_draft = True
                obj.save()
                if self.request.FILES.getlist('file'):
                    for f in self.request.FILES.getlist('file'):
                        Files.objects.create(article=obj, user=self.request.user, file=f)
            else:
                obj.save()
                if self.request.FILES.getlist('file'):
                    for f in self.request.FILES.getlist('files'):
                        Files.objects.create(article=obj, user=self.request.user, file=f)


            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class EditArticles(UpdateView):
    template_name = 'blog/edit-article.html'
    model = Article
    form_class = ArticleEditForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditArticles, self).dispatch(*args,**kwargs)

    def get_object(self, *args, **kwargs):
        object = super(EditArticles, self).get_object()
        if not object.user == self.request.user and not self.request.user.is_superuser:
            raise Http404
        return object


class DeleteArticle(BaseDeleteView):
    model = Article
    template_name = 'blog/delete-article-confirm.html'
    success_url = reverse_lazy('index_site')