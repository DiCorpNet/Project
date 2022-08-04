from django import forms

from .models import MyUser


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name','last_name','image', 'password', 'email', 'link_github', 'link_vk', 'about_us']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':"Введите своё имя"}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':"Введите свою фамилию"}),
            'about_us': forms.Textarea(attrs={'class':'form-control', 'placeholder':"Введите свою фамилию"}),
            'link_github': forms.TextInput(attrs={'class':'form-control'}),
            'link_vk': forms.TextInput(attrs={'class':'form-control'}),
        }

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Введите своё имя"}))