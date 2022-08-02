import os
import uuid
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from mptt.fields import TreeForeignKey
from app.models import Category
from .fields import WEBPField
from api.utils import comment_save
from django_ckeditor_5.fields import CKEditor5Field


def image_article(self, filename):
    return 'images/article/u_{0}/{1}.webp'.format(self.user.id, uuid.uuid4().hex)


def upload_file(self, filename):
    return 'upload/u_{0}/{1}'.format(self.user.id, filename)


def upload_file_post(self, filename):
    return 'upload/article/u_{0}/{1}'.format(self.user.id, filename)


def upload_file_comment(self, filename):
    return 'upload/comment/user_{0}/{1}'.format(self.user.id, filename)

class ArticleManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(content__icontains=query))
            qs = qs.filter(or_lookup)

        return qs

class CommentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = ( Q(content__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class Article(models.Model):
    TEMPLATE_PREVIEW = 'search/search-article.html'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Author', related_name='articles')
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description', max_length=1000)
    content = models.TextField('Full Content')
    category = TreeForeignKey(Category, on_delete=models.CASCADE , related_name='article_category')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_like', blank=True)
    image = WEBPField(verbose_name='Article Image', upload_to=image_article)
    slug = models.SlugField('Url adress', unique=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')

    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        indexes = [GinIndex(fields=['title'])]


    def likes_count(self):
        return self.likes.count()

    def likes_user(self):
        return self.likes.filter(id=self.user.id).exists()

    def get_absolute_url(self):
        return f"/blog/{self.category.slug}/{self.slug}/"

    def get_bookmark_count(self):
        return self.bookmark_article.all().count()




class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BookmarkArticles(BookmarkBase):
    class Meta:
        db_table = 'bookmark_article'

    obj = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE, related_name='bookmark_article')


class Comment(models.Model):
    TEMPLATE_PREVIEW = 'search/search-comment.html'
    class Meta:
        db_table = 'comments'
        indexes = [GinIndex(fields=['content'])]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_like', blank=True)
    file = models.FileField(upload_to=upload_file_comment, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return self.content[0:200]

    def likes_count(self):
        return self.likes.count()

    def likes_user(self):
        return self.likes.filter(id=self.user.id).exists()

    def filename(self):
        return os.path.basename(self.file.name)


class Files(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_file')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_file')
    file = models.FileField(upload_to=upload_file_post)
    secure = models.BooleanField(default=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file.name)


post_save.connect(comment_save, sender=Comment)
