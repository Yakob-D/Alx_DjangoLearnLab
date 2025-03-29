from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # Include authentication routes
    path('api/', include('posts.urls')),  # Include the posts API URLs
]
