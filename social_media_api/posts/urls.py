from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostFeedViewSet, PostViewSet

# Set up the router for viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'feed', PostFeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
