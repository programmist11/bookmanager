from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from locations.models import LocationRoot, Rack, Section


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Создаём библиотеку, стеллаж и полку
        self.root = LocationRoot.objects.create(name="Публичная библиотека")
        self.rack = Rack.objects.create(number=1, root=self.root)
        self.section = Section.objects.create(number=1, rack=self.rack)

        # Создаём книги
        self.book1 = Book.objects.create(
            title="Книга 1",
            author="Автор 1",
            year=2020,
            genre="Фантастика",
            isbn="1234567890123",
            total_copies=5,
            available_copies=5,
            location_root=self.root,
            rack=self.rack,
            section=self.section
        )
        self.book2 = Book.objects.create(
            title="Книга 2",
            author="Автор 2",
            year=2021,
            genre="Драма",
            isbn="9876543210123",
            total_copies=3,
            location_root=self.root,
            rack = self.rack,
            section = self.section
        # доступно будет автоматически 3
        )

    def test_book_list(self):
        url = reverse('book:book_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_book_detail(self):
        url = reverse('book:book_detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_book_create_with_defaults(self):
        url = reverse('book:book_list_create')
        data = {
            "title": "Новая книга",
            "author": "Автор 3",
            "year": 2023,
            "genre": "Приключения",
            "isbn": "1112223334445",
            "total_copies": 10,
            "location_root": self.root.id,
            "rack": self.rack.id,
            "section": self.section.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(isbn="1112223334445")
        # Проверяем автозаполнение available_copies
        self.assertEqual(book.available_copies, 10)
        # Проверяем, что rack и location_root установлены автоматически
        self.assertEqual(book.rack.id, self.rack.id)
        self.assertEqual(book.location_root.id, self.root.id)

    def test_books_by_root(self):
        url = reverse('book:books_by_root', args=[self.root.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data), 2)

    def test_books_by_rack(self):
        url = reverse('book:books_by_rack', args=[self.rack.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.book1.id)

    def test_books_by_section(self):
        url = reverse('book:books_by_section', args=[self.section.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.book1.id)

    def test_book_update(self):
        url = reverse('book:book_detail', args=[self.book1.id])
        data = {
            "title": "Новая книга",
            "author": "Автор 3",
            "year": 2023,
            "genre": "Приключения",
            "isbn": "1112223334445",
            "total_copies": 10,
            "location_root": self.root.id,
            "rack": self.rack.id,
            "section": self.section.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Новая книга")

    def test_book_delete(self):
        url = reverse('book:book_detail', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_book_autocomplete(self):
        url = reverse('book:book_autocomplete')
        response = self.client.get(url, {'title': 'Книга'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
