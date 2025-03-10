from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

#Created a serializer for the book model, includes all fields
#It also validates if the publication_year is not in the future
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def validate_publication_year(self, publication_year):
        current_year = datetime.now().year
        if publication_year > current_year:
            raise serializers.ValidationError('Publication year can not be in the future.')
        return publication_year

#Created a serializer for the Author model, that includes the name field
#It also includes a books field that is a nested BookSerializer, it's read only
#It will help serialize multiple related book instances for an author dynamically 
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name']