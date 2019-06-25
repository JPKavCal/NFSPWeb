from django import forms
from django.contrib.auth.models import User
from .models import UserCompanyInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompanyInfo
        exclude = ('user',)
