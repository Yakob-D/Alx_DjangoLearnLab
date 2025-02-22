# urls.py
from django.urls import path
from . import views  # Import the views module
from .views import list_books, LibraryDetailView  # Import specific views
from django.contrib.auth.views import LoginView, LogoutView  # Import built-in views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Use Django's built-in LoginView
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Use Django's built-in LogoutView
    path('register/', views.register, name='register'),  # Use views.register for the custom user_register view
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
]