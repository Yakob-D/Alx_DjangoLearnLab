from django.shortcuts import render
from rest_framework import generics, filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.admin = User.objects.create_superuser(username="admin", password="adminpassword")

        # Create sample books
        self.book1 = Book.objects.create(title="Django Basics", author="John Doe", publication_year=2020)
        self.book2 = Book.objects.create(title="Advanced Django", author="Jane Smith", publication_year=2021)
        self.book3 = Book.objects.create(title="Django REST", author="John Doe", publication_year=2019)

        # Define API endpoints
        self.book_list_url = "/api/books/"
        self.book_detail_url = f"/api/books/{self.book1.id}/"

    def test_list_books(self):
        """Test retrieving the list of books (unauthenticated users should have access)"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Check if all books are returned

    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        response = self.client.get(self.book_list_url, {"title": "Django Basics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django Basics")

    def test_search_books_by_author(self):
        """Test searching books by author"""
        response = self.client.get(self.book_list_url, {"search": "John Doe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books by John Doe

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year (ascending)"""
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2019)  # Oldest book first

    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year (descending)"""
        response = self.client.get(self.book_list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2021)  # Newest book first

    def test_create_book_unauthorized(self):
        """Test that unauthenticated users cannot create books"""
        data = {"title": "New Book", "author": "Author", "publication_year": 2023}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Test that authenticated users can create books"""
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "New Book", "author": "Author", "publication_year": 2023}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # Check if new book is added

    def test_retrieve_book_detail(self):
        """Test retrieving a book by ID"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Basics")

    def test_update_book_unauthorized(self):
        """Test that unauthenticated users cannot update a book"""
        data = {"title": "Updated Title"}
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test that authenticated users can update books"""
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "Updated Django Basics", "author": "John Doe", "publication_year": 2020}
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Django Basics")

    def test_delete_book_unauthorized(self):
        """Test that unauthenticated users cannot delete a book"""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete a book"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)  # One book should be deleted


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