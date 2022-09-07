from django.contrib import admin

# Register your models here.
from modeltranslation.admin import TranslationAdmin

from .forms import AdminBlogForm
from .models import Article, Files, Comment, UpdateArticle


class ArticleAdmin(TranslationAdmin):
    form = AdminBlogForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(Files)
admin.site.register(Comment)
admin.site.register(UpdateArticle)