from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Comment


class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(widget=forms.HiddenInput, required=False)
    comment_area = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control form-control-light mb-2", "rows": "3"}))
    # comment_area = forms.CharField(widget=CKEditor5Widget(config_name="comment"))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': "d-none"}), required=False, label='')