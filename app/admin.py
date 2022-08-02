from django.contrib import admin

# Register your models here.
from django_mptt_admin.admin import DjangoMpttAdmin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin

from .models import Category, Country, Location


class CategoryAdmin(DjangoMpttAdmin, TranslationAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(Country)
admin.site.register(Location)
