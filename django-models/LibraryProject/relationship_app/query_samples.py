from .models import Author, Book, Library, Librarian

author_name = 'James'
books_filtered = Book.objects.filter(author__name=author_name)  # Correcting the filter for author by name

library_name = 'Library Name'
library = Library.objects.get(name=library_name)  # Fetch the library object first
books = library.books.all()  # Get all books related to the library

librarian_name = 'Lily'
librarian = Librarian.objects.get(library__name=library_name)  # Fetch the librarian associated with the library
