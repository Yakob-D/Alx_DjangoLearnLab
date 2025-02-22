from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Library  # Ensure Library is imported
from django.views.generic import DetailView

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
