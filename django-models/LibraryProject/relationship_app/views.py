from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library  # Ensure Library is imported
from django.views.generic.detail import DetailView  # Correct import for DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Library  # Import your models
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

# Function-based View to List All Books
def list_books(request):
    # Retrieve all books from the database
    books = Book.objects.all()
    # Render the template with the list of books
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based View to Display Library Details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Update the template path
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Get all books related to the library
        return context

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the imported login function
            return redirect('home')  # Redirect to a home or dashboard page
    return render(request, 'relationship_app/login.html')  # Ensure this path is correct

def user_logout(request):
    auth_logout(request)  # Use the imported logout function
    return render(request, 'relationship_app/logout.html')  # Ensure this path is correct

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})
