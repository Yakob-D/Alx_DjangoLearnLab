from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books', null=True, blank=True)  # Reference to the custom user model

    def __str__(self):
        return self.title