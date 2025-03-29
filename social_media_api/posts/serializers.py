from rest_framework import serializers
from accounts.models import User
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Embed the user info (read-only)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']  # Author is read-only (set by authentication)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Embed the user info (read-only)
    post = PostSerializer(read_only=True)  # Embed the post info (read-only)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post']  # Author and post are read-only
