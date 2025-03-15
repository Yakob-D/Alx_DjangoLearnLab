from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# View to list books with filtering, searching, and ordering.
# Unauthenticated users have read-only access.
class BookListView(generics.ListAPIView):
    """
    API endpoint that allows users to list books with filtering, searching, and ordering.

    Features:
    - Filtering: Users can filter books by title, author, and publication_year.
    - Searching: Users can search books by title and author using partial matches.
    - Ordering: Users can order results by title or publication_year in ascending or descending order.

    Example API Requests:
    - GET /api/books/?title=SomeTitle -> Filters books by title.
    - GET /api/books/?author=SomeAuthor -> Filters books by author.
    - GET /api/books/?publication_year=2022 -> Filters books by publication year.
    - GET /api/books/?search=Harry -> Searches for books with "Harry" in the title or author.
    - GET /api/books/?ordering=title -> Orders books alphabetically by title (ascending).
    - GET /api/books/?ordering=-publication_year -> Orders books by publication year (newest first).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Adding filtering, searching, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields available for filtering
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields available for searching (partial match)
    search_fields = ['title', 'author']

    # Fields available for ordering (ascending or descending)
    ordering_fields = ['title', 'publication_year']
    
    # Default ordering
    ordering = ['title']

# View to retrieve a single book based on the ID.
# Unauthenticated users have read-only access.
class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a single book by its ID.

    Example API Request:
    - GET /api/books/1/ -> Retrieves the book with ID=1.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# View to create a book (Only authenticated users).
class BookCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new book. Only authenticated users can create books.

    Example API Request:
    - POST /api/books/ 
      {
          "title": "New Book",
          "author": "John Doe",
          "publication_year": 2023
      }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Custom validation before saving the book
    def perform_create(self, serializer):
        book = serializer.save()
        return book

# View to update a book (Only authenticated users).
class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update an existing book. Only authenticated users can update books.

    Example API Request:
    - PUT /api/books/1/
      {
          "title": "Updated Title",
          "author": "Jane Doe",
          "publication_year": 2024
      }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Custom validation before updating the book
    def perform_update(self, serializer):
        book = serializer.save()
        return book

# View to delete a book by filtering based on the title (Only authenticated users).
class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete books by title. Only authenticated users can delete books.

    Example API Request:
    - DELETE /api/books/?title=SomeTitle -> Deletes the book with the specified title.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        title_to_delete = self.request.query_params.get('title', None)
        if title_to_delete:
            return Book.objects.filter(title=title_to_delete)
        return Book.objects.none()
