from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        if user:
            post.author = user
        if commit:
            post.save()
        return post