import slug as slug
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import BaseDeleteView

from .forms import CreateFormPost, FilesCreateForm, ArticleEditForm
from .models import Article, Comment, Files
from app.models import Category

from api.forms import CommentForm

from api.mixins import NotificationsMixinDetail, NotificationsMixinList, BreadcrumbMixinList, BreadcrumbMixinDetail

from api.ipuser import get_info_bi_ip



class BlogList(ListView):
    pass


class BlogDetail(DetailView, BreadcrumbMixinDetail, NotificationsMixinDetail):
    model = Article
    slug_url_kwarg = 'article_slug'

    def get_queryset(self):
        category = self.kwargs.get('category_slug', '')
        q = Article.objects.filter(slug=self.kwargs.get('article_slug')).select_related('category').prefetch_related('comments')
        return q.filter(category__slug=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_comment'] = CommentForm()
        # get_info_bi_ip(ip=self.request.META.get('REMOTE_ADDR'))
        context['likes_user'] = context['article'].likes.filter(id=self.request.user.id).exists()
        context['files'] = Files.objects.filter(article=context['article'].id)
        context['comments'] = Comment.objects.filter(article_id=context['article'].id).prefetch_related('user', 'parent', "parent__user")
        return context


class BlogCategoryList(ListView, BreadcrumbMixinList, NotificationsMixinList):
    model = Article
    paginate_by = settings.PAGINATE

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs.get('cat_slug')).select_related('category').prefetch_related('user', 'comments', 'bookmark_article').order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Category.objects.get(slug=self.kwargs.get('cat_slug')).name
        return context


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