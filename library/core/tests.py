from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Book, Reader, BookLoan


class BookAddDeleteTests(TestCase):
    """Тесты добавления и удаления книг."""

    def setUp(self):
        self.client = Client()

    def test_add_book(self):
        """Добавление новой книги через форму: книга появляется в БД с правильными полями."""
        url = reverse("core:book_create")
        response = self.client.post(
            url,
            {"title": "Война и мир", "author": "Л. Толстой", "year": "1869"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get()
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Л. Толстой")
        self.assertEqual(book.year, 1869)

    def test_add_book_empty_year_ok(self):
        """Добавление книги без года издания: год может быть пустым."""
        url = reverse("core:book_create")
        response = self.client.post(
            url,
            {"title": "Книга без года", "author": "Автор", "year": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get()
        self.assertIsNone(book.year)

    def test_delete_book(self):
        """Удаление книги по POST: книга исчезает из БД."""
        book = Book.objects.create(title="Удаляемая", author="Автор", year=2000)
        url = reverse("core:book_delete", kwargs={"pk": book.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_get_shows_confirm(self):
        """Страница удаления книги (GET) показывает подтверждение с названием книги."""
        book = Book.objects.create(title="Удаляемая", author="Автор")
        url = reverse("core:book_delete", kwargs={"pk": book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(book.title, response.content.decode())


class IssueReturnTests(TestCase):
    """Тесты выдачи и возврата книг."""

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Книга", author="Автор")
        self.reader = Reader.objects.create(name="Иван Иванов")

    def test_issue_book(self):
        """Выдача книги читателю: создаётся запись выдачи, книга числится на руках."""
        url = reverse("core:issue_create")
        response = self.client.post(
            url,
            {"book": self.book.pk, "reader": self.reader.pk},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookLoan.objects.count(), 1)
        loan = BookLoan.objects.get()
        self.assertEqual(loan.book, self.book)
        self.assertEqual(loan.reader, self.reader)
        self.assertIsNone(loan.returned_at)

    def test_return_book(self):
        """Возврат книги: у записи выдачи проставляется дата возврата."""
        loan = BookLoan.objects.create(book=self.book, reader=self.reader)
        url = reverse("core:issue_return", kwargs={"pk": loan.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertIsNotNone(loan.returned_at)

    def test_after_return_book_available_for_issue_again(self):
        """После возврата книга снова появляется в списке доступных для выдачи."""
        loan = BookLoan.objects.create(book=self.book, reader=self.reader)
        url_return = reverse("core:issue_return", kwargs={"pk": loan.pk})
        self.client.post(url_return, follow=True)
        url_issue = reverse("core:issue_create")
        response = self.client.get(url_issue)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn(self.book, form.fields["book"].queryset)

    def test_issued_book_not_in_issue_form_choices(self):
        """Выданная книга не показывается в выборе книги при новой выдаче."""
        BookLoan.objects.create(book=self.book, reader=self.reader)
        url = reverse("core:issue_create")
        response = self.client.get(url)
        form = response.context["form"]
        self.assertNotIn(self.book, form.fields["book"].queryset)
