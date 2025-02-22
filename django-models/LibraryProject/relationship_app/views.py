from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.views.generic import DetailView
from .models import Library

# Create your views here.
def list_books(request):
    # Retrieve all books from the database
    books = Book.objects.all()
    
    # Create a response string with book titles and authors
    response_str = "<h1>List of Books</h1><ul>"
    for book in books:
        response_str += f"<li>{book.title} by {book.author.name}</li>"
    response_str += "</ul>"

    return HttpResponse(response_str)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context