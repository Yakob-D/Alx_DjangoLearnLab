from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

class ExampleForm(forms.Form):  # Create the ExampleForm
    user_input = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter your text'}))
