from django.contrib import admin
from .models import Book, Reader, BookLoan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ("book", "reader", "issued_at", "returned_at")
    list_filter = ("returned_at",)
