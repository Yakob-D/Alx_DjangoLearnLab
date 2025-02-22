# urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from .views import user_login, user_logout, user_register
from django.contrib.auth.views import LoginView, LogoutView  # Add this import

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Use LoginView with template
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Use LogoutView with template
    path('register/', user_register, name='register'),
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
]
