# urls.py
from django.urls import path
from .views import list_books, LibraryDetailView, user_register  # Ensure user_register is imported
from django.contrib.auth.views import LoginView, LogoutView  # Import built-in views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Use Django's built-in LoginView
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Use Django's built-in LogoutView
    path('register/', user_register, name='register'),  # Keep your custom user_register view
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
]
