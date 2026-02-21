from django.db import models


class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=200)
    year = models.PositiveIntegerField("Год издания", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"


class Reader(models.Model):
    name = models.CharField("ФИО", max_length=200)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    issued_at = models.DateTimeField("Дата выдачи", auto_now_add=True)
    returned_at = models.DateTimeField("Дата возврата", null=True, blank=True)

    class Meta:
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"
        ordering = ["-issued_at"]

    def __str__(self):
        status = "возвращена" if self.returned_at else "на руках"
        return f"{self.book} → {self.reader} ({status})"

    @property
    def is_returned(self):
        return self.returned_at is not None
