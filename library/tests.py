import unittest
import os
import json
from main import Book, Library


class TestBook(unittest.TestCase):
    def test_to_dict(self):
        book = Book(1, "Test Title", "Test Author", 2020, "в наличии")
        expected = {
            "id": 1,
            "title": "Test Title",
            "author": "Test Author",
            "year": 2020,
            "status": "в наличии",
        }
        self.assertEqual(book.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "id": 1,
            "title": "Test Title",
            "author": "Test Author",
            "year": 2020,
            "status": "в наличии",
        }
        book = Book.from_dict(data)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.status, "в наличии")


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Создает временный файл перед каждым тестом."""
        self.test_file = "test_library.json"
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump([], file)

        self.library = Library(self.test_file)

    def tearDown(self):
        """Удаляет временный файл после каждого теста."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")

    def test_delete_book(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        book_id = self.library.books[0].id
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        results = self.library.search_books("Test Title", "title")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Title")

    def test_update_status(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_find_book_by_id(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        book_id = self.library.books[0].id
        book = self.library.find_book_by_id(book_id)
        self.assertIsNotNone(book)
        self.assertEqual(book.id, book_id)

    def test_load_data(self):
        data = [
            {
                "id": 1,
                "title": "Loaded Title",
                "author": "Loaded Author",
                "year": 2020,
                "status": "в наличии",
            }
        ]
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(data, file)

        self.library.load_data()
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Loaded Title")

    def test_save_data(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        self.library.save_data()

        with open(self.test_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Title")


if __name__ == "__main__":
    unittest.main()
