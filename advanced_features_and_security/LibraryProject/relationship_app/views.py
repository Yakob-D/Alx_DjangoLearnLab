from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.detail import DetailView
from django.conf import settings  # Updated import for custom user model
from .models import Book, Library, UserProfile  # Ensure UserProfile is imported

# Function-based View to List All Books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based View to Display Library Details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
    return render(request, 'relationship_app/login.html')

def user_logout(request):
    auth_logout(request)
    return render(request, 'relationship_app/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='Member')  # Ensure UserProfile is created
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        # Instead of using BookForm, handle the book creation manually
        title = request.POST.get('title')
        author = request.POST.get('author')
        # Add any other fields as needed
        if title and author:  # Ensure required fields are filled
            Book.objects.create(title=title, author=author)  # Adjust fields accordingly
            return redirect('book_list')
    return render(request, 'books/add_book.html')  # Adjust template as needed

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        # Instead of using BookForm, update the book directly
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        # Add any other fields as needed
        book.save()
        return redirect('book_list')
    return render(request, 'books/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})
