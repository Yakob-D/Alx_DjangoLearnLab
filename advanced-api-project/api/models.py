from django.db import models

#Created an Author model that will store the name of authors
class Author(models.Model):
    name = models.CharField(max_length=200)

#Created a Book model that will store the title, publication_year of books
#It also have a foreignkey author to create a one to many relationship between my Book table and Author table in my database
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name = 'books')