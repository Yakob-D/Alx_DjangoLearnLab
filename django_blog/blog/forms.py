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

class TagWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        tags = Tag.objects.all()
        output = ''
        for tag in tags:
            checked = 'checked' if tag.id in value else ''
            output += f'<label><input type="checkbox" name="{name}" value="{tag.id}" {checked}> {tag.name}</label><br>'
        return output

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        widget=TagWidget(),  # Use the custom TagWidget
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        if user:
            post.author = user
        if commit:
            post.save()

            # Save tags
            if self.cleaned_data['tags']:
                tags = self.cleaned_data['tags'].split(',')
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    post.tags.add(tag)

            post.save()
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