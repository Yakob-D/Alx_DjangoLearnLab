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
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        if user:
            post.author = user

        if commit:
            post.save()
            self.save_tags(post)

        return post

    def save_tags(self, post):
        """Handles creating or associating tags with the post."""
        tag_names = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tag_names.split(',') if tag.strip()]

        post.tags.clear()  # Remove old tags
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

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