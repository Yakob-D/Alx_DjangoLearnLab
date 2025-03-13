# Import necessary modules from Django and views from the current app
from django.urls import path
from .views import (
    BookCreateView, BookListView, BookDeleteView, BookUpdateView, BookDetailView
)

# Define the URL patterns for the API endpoints
urlpatterns = [
    # URL for listing all books, accessible via GET request
    path('books/', BookListView.as_view(), name='book-list'),

    # URL for deleting a specific book, accessible via DELETE request
    path('books/delete', BookDeleteView.as_view(), name='book-delete'),

    # URL for updating a specific book, accessible via PUT/PATCH request
    path('books/update', BookUpdateView.as_view(), name='book-update'),

    # URL for creating a new book, accessible via POST request
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # URL for retrieving the details of a specific book by its primary key (pk)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail')
]
