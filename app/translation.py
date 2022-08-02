from modeltranslation.translator import register, TranslationOptions
from .models import Category, Country, Location

@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)

@register(Country)
class CountryTranslationOption(TranslationOptions):
    fields = ('name',)

@register(Location)
class LocationTranslationOption(TranslationOptions):
    fields = ('name',)