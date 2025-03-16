from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }
        self.book = Book.objects.create(**self.book_data)

    def test_create_book_authenticated(self):
        # Test creating a book when authenticated
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023
        }
        self.client.login(username='testuser', password='password')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Ensure one book has been added.

    def test_create_book_unauthenticated(self):
        # Test creating a book when not authenticated
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_book_list_authenticated(self):
        # Test GET request on book list endpoint when authenticated
        url = reverse('book-list')
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Book', response.data[0]['title'])

    def test_get_book_detail_authenticated(self):
        # Test GET request for a single book detail
        url = reverse('book-detail', args=[self.book.id])
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book_authenticated(self):
        # Test updating a book when authenticated
        url = reverse('book-detail', args=[self.book.id])
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'publication_year': 2022
        }
        self.client.login(username='testuser', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book_authenticated(self):
        # Test deleting a book when authenticated
        url = reverse('book-detail', args=[self.book.id])
        self.client.login(username='testuser', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        # Test filtering books by title
        url = reverse('book-list') + '?title=Test Book'
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        # Test searching books by author
        url = reverse('book-list') + '?search=Test Author'
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        # Test ordering books by publication year
        url = reverse('book-list') + '?ordering=publication_year'
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
