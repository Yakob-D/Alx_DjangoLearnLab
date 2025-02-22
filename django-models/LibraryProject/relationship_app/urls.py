# urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from .views import user_login, user_logout, user_register

urlpatterns = [
    path('login/', user_login, name='login'),  # Use your custom user_login view
    path('logout/', user_logout, name='logout'),  # Use your custom user_logout view
    path('register/', user_register, name='register'),  # Use your custom user_register view
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
]