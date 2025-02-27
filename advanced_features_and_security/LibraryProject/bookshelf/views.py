# views.py

from django.shortcuts import render
from .models import Book
from .forms import BookForm  # Ensure you're importing the correct form
from .forms import ExampleForm
from django.core.exceptions import PermissionDenied  # Import raise_exception equivalent

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Use form's save method to prevent SQL injection
            # Redirect or provide a success message if needed
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

# Add a view example for raise_exception
def some_view(request):
    if not request.user.is_authenticated:
        raise PermissionDenied  # Equivalent to raise_exception
    # Your view logic here
