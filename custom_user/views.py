from django.views.generic import ListView, DetailView, TemplateView

from .models import MyUser
from blog.models import Article, Comment, Files


class ProfileAllList(ListView):
    model = MyUser
    paginate_by = 5


class ProfileUser(TemplateView):
    template_name = 'custom_user/profile-user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = MyUser.objects.get(username=self.kwargs.get('user_slug'))
        # context['form'] = UserFormUpdate(instance=self.request.user)
        return context


class ProfileUserArticle(ListView):
    template_name = 'custom_user/profile-user-article.html'

    def get_queryset(self):
        result = Article.objects.filter(user__username=self.kwargs.get('user_slug')).order_by('-id')
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['profile'] = MyUser.objects.get(username=self.kwargs.get('user_slug'))
        return context

class ProfileUserComments(ListView):
    template_name = 'custom_user/profile-user-comments.html'

    def get_queryset(self):
        result = Comment.objects.filter(user_id__username=self.kwargs.get('user_slug')).order_by('-id')
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['profile'] = MyUser.objects.get(username=self.kwargs.get('user_slug'))
        return context

class ProfileUserFiles(ListView):
    model = Files
    template_name = 'custom_user/filemanager.html'

    def get_queryset(self):
        result = Files.objects.filter(user__username=self.kwargs.get('user_slug'))
        return result