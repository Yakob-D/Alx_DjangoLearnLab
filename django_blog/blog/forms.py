from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Using checkbox selection for tags
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),  # Ensure this part is properly defined
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        if user:
            post.author = user
        if commit:
            post.save()
            self.save_m2m()  # Make sure many-to-many relationships (tags) are saved
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['content'].widget = forms.Textarea(attrs={'rows':4, 'cols':50})
        
        def save(self, commit=True, user=None, post=None):
            comment = super().save(commit=False)

            if user:
                comment.author = user
            if post:
                comment.post = post
            if commit:
                comment.save()
            return comment

        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content) < 5:
                raise forms.ValidationError('Comment must be at least 5 characters long.')
            return content