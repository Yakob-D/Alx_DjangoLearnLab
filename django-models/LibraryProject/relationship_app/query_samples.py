from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name=author_name)  # Fetch the Author instance
books_filtered = Book.objects.filter(author=author)  # Use the Author instance to filter books

# List all books in a library
library = Library.objects.get(name=library_name)  # Fetch the Library instance
books = library.books.all()  # Get all books related to the library

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)  # Get the Librarian instance for the Library
