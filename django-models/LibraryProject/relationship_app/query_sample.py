from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = 'James'
try:
    # Get the Author instance
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)  # Filter books by the Author instance
except Author.DoesNotExist:
    books_by_author = []  # Handle case where author doesn't exist
    print(f"Author '{author_name}' does not exist.")

# List all books in a library
library_name = 'Library Name'
try:
    # Get the Library instance
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()  # Get all books associated with the Library instance
except Library.DoesNotExist:
    books_in_library = []  # Handle case where library doesn't exist
    print(f"Library '{library_name}' does not exist.")

# Retrieve the librarian for a library
try:
    # Get the Librarian instance associated with the Library instance
    librarian = Librarian.objects.get(library=library)
except Librarian.DoesNotExist:
    librarian = None  # Handle case where librarian doesn't exist
    print(f"No librarian found for the library '{library_name}'.")
