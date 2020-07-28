from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    photo = forms.ImageField()
    name = forms.CharField()
    name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    photo.widget.attrs.update({'class': 'input-group-text'})

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'photo']


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    email.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['password']
