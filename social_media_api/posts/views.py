from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination  # Apply pagination to Post view
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the author as the current logged-in user
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            # Only allow users to edit or delete their own comments
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()
