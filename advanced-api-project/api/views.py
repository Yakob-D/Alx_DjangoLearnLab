from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# View to list books after filtering the data based on the title, read-only access given to un authenticated users
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticatedOrReadOnly]
    filer_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'publication_year']
# View to retrieve a single book based on the ID, read-only access given to any un authenticated users
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serialzier_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# View to create books and push the data on to the database after validation, access given to authenticated users only
class BookCreateView(generics.CreateAPIView):
    queryset = Book.object.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # For validation on the data before create
    def perform_create(self, serializer):
        book = serializer.save()
        return book

# View to update books and push the data on to the database after validation, access given to authenticated users only
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.object.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # For validation on the data before update
    def perform_update(self, serializer):
        book = serializer.save()
        return book

# View to delete books by filtering based on title, access given to authenticated users only
class BookDeleteView(generics.DestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        title_to_delete = self.request.query_params.get('title', None)
        if title_to_delete:
            return Book.objects.filter(title = title_to_delete)
        return Book.objects.none()