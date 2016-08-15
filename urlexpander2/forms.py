from django import forms
from .models import Url
from django.contrib.auth.models import User

class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['shortened']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']