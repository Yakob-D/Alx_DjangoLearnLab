from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = 'James'  # Replace this with the actual author's name in your database
try:
    author = Author.objects.get(name=author_name)  # Get the Author instance
    books_by_author = Book.objects.filter(author=author)  # Query books by the author
except Author.DoesNotExist:
    books_by_author = []  # No books if the author doesn't exist

# List all books in a library
library_name = 'Library Name'  # Replace with the actual library's name
try:
    library = Library.objects.get(name=library_name)  # Get the Library instance
    books_in_library = library.books.all()  # Query all books in the library
except Library.DoesNotExist:
    books_in_library = []  # No books if the library doesn't exist

# Retrieve the librarian for a library
try:
    librarian = Librarian.objects.get(library=library)  # Get the Librarian instance
except Librarian.DoesNotExist:
    librarian = None  # No librarian if the library doesn't exist
