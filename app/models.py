from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField('Category', max_length=50)
    slug = models.SlugField('Slug Category', max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name='Parent Category', on_delete=models.PROTECT, db_index=True, null=True, blank=True, related_name='category_children')
    icon = models.CharField('Icon', max_length=50, null=True, blank=True)
    base = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Категория'

    def get_absolute_url(self):
        return f'/blog/{self.slug}/'


class Country(models.Model):
    name = models.CharField('Country name', max_length=50)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField('User Lang', max_length=50)

    def __str__(self):
        return self.name

