from modeltranslation.translator import register, TranslationOptions
from .models import MyUser


@register(MyUser)
class UserTranslationOptions(TranslationOptions):
    fields = ('about_us',)