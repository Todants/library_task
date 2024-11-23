import json
import os
import sys
from typing import List, Dict, Optional


class Book:
    """Класс для представления книги."""
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """Возвращает словарь с данными книги."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict):
        """Создает объект книги из словаря."""
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )


class Library:
    """Класс для управления библиотекой."""
    def __init__(self, data_file: str):
        self.DATA_FILE = data_file
        self.books: List[Book] = []
        self.load_data()

    def load_data(self) -> None:
        """Загружает книги из JSON файла."""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                try:
                    self.books = [Book.from_dict(book) for book in data]
                except KeyError:
                    print("[ERROR] Испорченные данные. Исправьте ошибку в данных или используйте другой файл.")
                    sys.exit(1)
        else:
            with open(self.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            self.books = []

    def save_data(self) -> None:
        """Сохраняет книги в JSON файл."""
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4, ensure_ascii=False)

    def generate_id(self) -> int:
        """Генерирует уникальный ID для новой книги."""
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        new_book = Book(book_id=self.generate_id(), title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_data()
        print("Книга успешно добавлена!")

    def delete_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки."""
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_data()
            print("Книга успешно удалена!")
        else:
            print("[ERROR] Книга с указанным ID не найдена.")

    def search_books(self, query: str, field: str) -> List[Book]:
        """Ищет книги по указанному полю."""
        return [book for book in self.books if str(getattr(book, field, "")).lower() == query.lower()]

    def print_books(self, books: Optional[List[Book]] = None) -> None:
        """Выводит список книг."""
        if books is None:
            books = self.books
        if not books:
            print("Библиотека пуста.")
            return
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
        print("-" * 75)
        for book in books:
            print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")

    def update_status(self, book_id: int, status: str) -> None:
        """Обновляет статус книги."""
        book = self.find_book_by_id(book_id)
        if book:
            book.status = status
            self.save_data()
            print("Статус книги успешно обновлён!")
        else:
            print("[ERROR] Книга с указанным ID не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """Находит книгу по ID."""
        for book in self.books:
            if book.id == book_id:
                return book
        return None


def main():
    """Главная функция."""
    data_file = sys.argv[1] if len(sys.argv) > 1 else "library.json"
    print(f"Данные для библиотеки взяты из файла {data_file}")
    library = Library(data_file)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
            except ValueError:
                print("[ERROR] Некорректно указан год.")
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги: "))
                library.delete_book(book_id)
            except ValueError:
                print("[ERROR] Некорректный ID.")
        elif choice == "3":
            field = input("Искать по (title, author, year): ").strip()
            if field not in {"title", "author", "year"}:
                print("[ERROR] Некорректное поле поиска.")
                continue
            query = input("Введите значение для поиска: ")
            results = library.search_books(query, field)
            library.print_books(results)
        elif choice == "4":
            library.print_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
                status = input("Введите новый статус (в наличии/выдана): ").strip()
                if status not in {"в наличии", "выдана"}:
                    print("[ERROR] Некорректный статус.")
                    continue
                library.update_status(book_id, status)
            except ValueError:
                print("[ERROR] Некорректный ID.")
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("[ERROR] Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
