from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from .models import Book

# Django REST Framework Views for handling book-related API requests.
# Permissions are configured to ensure only authenticated users can access the API.

class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of books.

    - Uses Django REST Framework's `ListAPIView`, which provides a read-only endpoint.
    - Requires authentication (users must be logged in with a valid token or session).
    - Uses the `BookSerializer` to serialize Book objects.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint.

class BookViewSet(viewsets.ModelViewSet):
    """
    API view to perform CRUD (Create, Read, Update, Delete) operations on books.

    - Uses Django REST Framework's `ModelViewSet`, which provides full CRUD functionality.
    - Requires authentication (users must be logged in with a valid token or session).
    - Uses the `BookSerializer` to handle serialization.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint.
