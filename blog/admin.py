from django.contrib import admin

# Register your models here.
from modeltranslation.admin import TranslationAdmin

from .forms import AdminBlogForm
from .models import Article, Files


class ArticleAdmin(TranslationAdmin):
    form = AdminBlogForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(Files)