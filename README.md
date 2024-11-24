# Задание: Разработка системы управления библиотекой

Этот проект представляет собой консольное приложение для управления библиотекой, где можно добавлять, удалять, искать книги, изменять их статус и отображать список всех книг. Программа написана на Python и использует JSON для хранения данных.

## Запуск приложения

Склонируйте проект на свой компьютер или скачайте и распакуйте zip-архивю
``` bash
git clone https://github.com/Todants/library_task.git
```
Перейдите в папку с проектом.
``` bash
cd library
```
Для запуска используй команду
``` bash
python main.py your_file.json
```
Вместо your_file.json нужно указать название файла, из которого хотите брать данные. Если не указывать файл, будет использован файл по умолчанию - library.json. Если файла не сущесвует, он будет создан.

Для запуска тестов нужно выполнить команду
``` bash
python .\tests.py -v
```

## Основной функционал

### Объект Книга
Класс Book. Реализует создание объекта книги, преобразование словаря в объект класса Book и наоборот.

### Объект Библиотека

Класс Library. Реализует загрузку данных из JSON файла, сохранение данных в JSON файл, добавление книг, удаление книг, поиск книг, изменение статуса книг, отображение книг.
Ниже представлена подробная информация:

### 1. Добавление книги
- Пользователь вводит название книги, автора и год издания.
- Книга получает уникальный `ID` и статус "в наличии" по умолчанию.
- Код, реализующий данный функционал:
  ``` py
  def add_book(self, title: str, author: str, year: int) -> None:
      """Добавляет книгу в библиотеку."""
      new_book = Book(book_id=self.generate_id(), title=title, author=author, year=year)
      self.books.append(new_book)
      self.save_data()
      print("Книга успешно добавлена!")
  ```
- Пример использования:
  
  ![image](https://github.com/user-attachments/assets/ef2560e7-393e-4324-88e3-1dfc5abc86f7)

### 2. Удаление книги
 - Пользователь вводит id книги, которую нужно удалить.
 - Если книга с таким id найдена, она удаляется.
 - Код, реализующий данный функционал:
   ``` py
   def delete_book(self, book_id: int) -> None:
       """Удаляет книгу из библиотеки."""
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_data()
            print("Книга успешно удалена!")
        else:
            print("[ERROR] Книга с указанным ID не найдена.")
   ```
  - Пример использования:

    ![image](https://github.com/user-attachments/assets/3ace85e1-1dc2-410a-8d18-277dbcb4911b)

### 3. Поиск книги
  - Пользователь выбирает, по каком полю искать: title, author или year.
  - Пользователь вводит значение длля выбранного поля.
  - Если по выбранным фильтрам найдены книги - они выводятся.
  - Код, реализующий данный функционал:
    ``` py
    def search_books(self, query: str, field: str) -> List[Book]:
        """Ищет книги по указанному полю."""
        return [book for book in self.books if str(getattr(book, field, "")).lower() == query.lower()]
    ```
  - Пример использования:

    ![image](https://github.com/user-attachments/assets/b8dceaa7-ae32-4893-ab88-4cf4a5160822)

### 4. Отображение всех книг
  - Приложение выводит список всех книг с их id, title, author, year и status.
  - Код, реализующий данный функционал:
    ``` py 
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
    ```
  - Пример использования:
    
    ![image](https://github.com/user-attachments/assets/e5157b09-ed64-4eda-8135-e98d30faf28b)

### 5. Изменение статуса книги
  - Пользователь вводит id книги и новый статус (“в наличии” или “выдана”).
  - Если книга с таким id найдена, её статус приравнивается к указанному значению.
  - Код, реализующий данный функционал:
    ``` py 
    def update_status(self, book_id: int, status: str) -> None:
        """Обновляет статус книги."""
        book = self.find_book_by_id(book_id)
        if book:
            book.status = status
            self.save_data()
            print("Статус книги успешно обновлён!")
        else:
            print("[ERROR] Книга с указанным ID не найдена.")
    ```
  - Пример использования:

    ![image](https://github.com/user-attachments/assets/1c238df9-47b4-4c3d-877e-7b8492f6a15b)

-----

Контакты: https://t.me/bylygeme

