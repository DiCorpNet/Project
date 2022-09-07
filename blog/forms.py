from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Article


class AdminBlogForm(forms.ModelForm):
     content = forms.CharField(widget=CKEditor5Widget(config_name="extends"))

class CreateFormPost(forms.ModelForm):
     
     def __init__(self,*args, **kwargs):
          super(CreateFormPost, self).__init__(*args, **kwargs)
          self.fields['content'].required = False
          
     
     slug = forms.SlugField(label='URL (заполняется автоматически)' ,widget=forms.TextInput(
          attrs={"class": "form-control", "placeholder": "Slug", "aria-label": "Slug", 'readonly': True}))


     class Meta:
          model = Article
          exclude = ('user', 'likes', 'create_at', 'file', 'is_new' )
          fields = '__all__'

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control'}),
               'category': forms.Select(
                attrs={'class': 'form-select', 'aria-label': 'Выберите категорию', "name": "category",
                       'required': True}),
               'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"},config_name="extends" )
          }
          labels = {
               'title': 'Titles is titles',
          }

          help_texts = {
               'title': 'Some useful help text.',
          }


class FilesCreateForm(forms.Form):
     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class ArticleEditForm(forms.ModelForm):
     class Meta:
          model = Article
          fields = ['title', 'slug', 'content', 'category', 'image']

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
               'category': forms.Select(
                    attrs={'class': 'form-select', 'aria-label': 'Выберите категорию', "name": "category",
                           'required': True}),
          }

     slug = forms.SlugField(widget=forms.TextInput(
          attrs={"class": "form-control", "placeholder": "Slug", "aria-label": "Slug", 'readonly': True}))
     content = forms.CharField(widget=CKEditor5Widget(config_name="extends"), required=False)

