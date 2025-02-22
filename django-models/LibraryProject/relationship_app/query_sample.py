from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = 'James'
author = Author.objects.get(name=author_name)  # Ensure the author exists
books_by_author = Book.objects.filter(author=author)  # Filter books by the Author instance

# List all books in a library
library_name = 'Library Name'
library = Library.objects.get(name=library_name)  # Ensure the library exists
books_in_library = library.books.all()  # Get all books in the library

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)  # Get the librarian for the specific Library instance
