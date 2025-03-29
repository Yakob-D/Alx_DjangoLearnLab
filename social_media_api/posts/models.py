# posts/models.py
from django.db import models
from accounts.models import User  # Import the custom User model
from django.utils import timezone  # To handle timestamps

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # ForeignKey to Post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # ForeignKey to User (author)
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update on modification

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
