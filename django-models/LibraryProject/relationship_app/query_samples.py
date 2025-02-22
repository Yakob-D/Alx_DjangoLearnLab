from .models import Author, Book, Library, Librarian

author_name = 'James'
books_filtered = Book.objects.filter(author=author_name)

library_name = 'Library Name'
books = Book.objects.filter(name=library_name)

librarian_name = 'Lily'
librarian = Librarian.objects.get(name=librarian_name)
