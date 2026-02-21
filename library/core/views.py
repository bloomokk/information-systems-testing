from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from .models import Book, Reader, BookLoan
from .forms import BookForm, ReaderForm, IssueBookForm


def home(request):
    return redirect("core:book_list")


class BookListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "core/book_list.html"
    paginate_by = 15


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Книга добавлена.")
            return redirect("core:book_list")
    else:
        form = BookForm()
    return render(request, "core/book_form.html", {"form": form, "title": "Добавить книгу"})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Книга сохранена.")
            return redirect("core:book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "core/book_form.html", {"form": form, "title": "Редактировать книгу"})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Книга удалена.")
        return redirect("core:book_list")
    return render(request, "core/book_confirm_delete.html", {"book": book})


class ReaderListView(ListView):
    model = Reader
    context_object_name = "readers"
    template_name = "core/reader_list.html"
    paginate_by = 15


def reader_create(request):
    if request.method == "POST":
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Читатель зарегистрирован.")
            return redirect("core:reader_list")
    else:
        form = ReaderForm()
    return render(request, "core/reader_form.html", {"form": form, "title": "Регистрация читателя"})


def reader_edit(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    if request.method == "POST":
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные читателя сохранены.")
            return redirect("core:reader_list")
    else:
        form = ReaderForm(instance=reader)
    return render(request, "core/reader_form.html", {"form": form, "title": "Редактировать читателя"})


def issue_list(request):
    active = BookLoan.objects.filter(returned_at__isnull=True).select_related("book", "reader")
    return render(request, "core/issue_list.html", {"loans": active})


def issue_create(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Книга выдана.")
            return redirect("core:issue_list")
    else:
        form = IssueBookForm()
    return render(request, "core/issue_form.html", {"form": form, "title": "Выдать книгу"})


def issue_return(request, pk):
    loan = get_object_or_404(BookLoan, pk=pk, returned_at__isnull=True)
    if request.method == "POST":
        from django.utils import timezone
        loan.returned_at = timezone.now()
        loan.save()
        messages.success(request, "Книга возвращена.")
        return redirect("core:issue_list")
    return render(request, "core/issue_confirm_return.html", {"loan": loan})
