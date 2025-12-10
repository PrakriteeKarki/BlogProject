from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Post,Comment

class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','caption','image']


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']