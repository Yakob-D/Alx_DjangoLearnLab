from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        }
        self.book = Book.objects.create(**self.book_data)
        self.book_url = '/api/books/'

    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.book_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication"""
        response = self.client.post(self.book_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_books_list(self):
        """Test getting the list of books with search, filter, and ordering"""
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Book', str(response.data))

    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        response = self.client.get(self.book_url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(self.book_url, {'author': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Test Author')

    def test_search_books(self):
        """Test searching books by title or author"""
        response = self.client.get(self.book_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Book', str(response.data))

    def test_order_books_by_title(self):
        """Test ordering books by title"""
        Book.objects.create(title='A Book', author='Author A', publication_year=2022)
        response = self.client.get(self.book_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'A Book')

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year"""
        Book.objects.create(title='Old Book', author='Old Author', publication_year=2020)
        response = self.client.get(self.book_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2023)

    def test_get_book_detail(self):
        """Test getting a single book's details"""
        url = f'/api/books/{self.book.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.client.login(username='testuser', password='password')
        url = f'/api/books/{self.book.id}/'
        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2024
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')

    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication"""
        url = f'/api/books/{self.book.id}/'
        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2024
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.login(username='testuser', password='password')
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication"""
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
