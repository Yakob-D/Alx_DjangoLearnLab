# urls.py
from django.urls import path
from . import views  # Import the views module
from .views import list_books, LibraryDetailView  # Import specific views
from django.contrib.auth.views import LoginView, LogoutView  # Import built-in views
from .admin_view import Admin
from .librarian_view import Librarian
from .member_view import Member
from .views import add_book, edit_book, delete_book

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Use Django's built-in LoginView
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Use Django's built-in LogoutView
    path('register/', views.register, name='register'),  # Use views.register for the custom user_register view
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
    path('admin-view/', Admin, name='admin_view'),
    path('librarian_view/', Librarian, name='librarian_view'),
    path('member_view/', Member, name='member_view'),
    path('add_book/', add_book, name='add_book'),  # Updated to match the exact expected path
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),  # Updated to match expected path
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
]