# chatbot_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password')
    password2=forms.CharField(label='Confirm Password (again)')
    email=forms.CharField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
            

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput)
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput())

from .models import Cluster

class ClusterForm(forms.ModelForm):
    class Meta:
        model = Cluster
        fields = ['name', 'pdf_file', 'openai_api_key']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  # Set the user to the logged-in user
        if commit:
            instance.save()
        return instance