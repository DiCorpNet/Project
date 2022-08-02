from django import forms

#
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Article


class AdminBlogForm(forms.ModelForm):

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["description"].required = False

     description = forms.CharField(widget=CKEditor5Widget( config_name="extends"))
     content = forms.CharField(widget=CKEditor5Widget( config_name="extends"))

class CreateFormPost(forms.ModelForm):
     slug = forms.SlugField(widget=forms.TextInput(
          attrs={"class": "form-control", "placeholder": "Slug", "aria-label": "Slug", 'readonly': True}))
     description = forms.CharField(widget=CKEditor5Widget(config_name="extends"), required=False)
     content = forms.CharField(widget=CKEditor5Widget(config_name="extends"), required=False)


     class Meta:
          exclude = ('user', 'likes', 'create_at', 'file' )
          fields = '__all__'
          model = Article

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control'}),
               'category': forms.Select(
                attrs={'class': 'form-select', 'aria-label': 'Выберите категорию', "name": "category",
                       'required': True}),
          }


class FilesCreateForm(forms.Form):
     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class ArticleEditForm(forms.ModelForm):
     class Meta:
          model = Article
          fields = ['title', 'slug', 'description', 'content', 'category']

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
               'category': forms.Select(
                    attrs={'class': 'form-select', 'aria-label': 'Выберите категорию', "name": "category",
                           'required': True}),
          }

     slug = forms.SlugField(widget=forms.TextInput(
          attrs={"class": "form-control", "placeholder": "Slug", "aria-label": "Slug", 'readonly': True}))
     description = forms.CharField(widget=CKEditor5Widget(config_name="extends"), required=False)
     content = forms.CharField(widget=CKEditor5Widget(config_name="extends"), required=False)

