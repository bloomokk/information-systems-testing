from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("readers/", views.ReaderListView.as_view(), name="reader_list"),
    path("readers/add/", views.reader_create, name="reader_create"),
    path("readers/<int:pk>/edit/", views.reader_edit, name="reader_edit"),
    path("issues/", views.issue_list, name="issue_list"),
    path("issues/issue/", views.issue_create, name="issue_create"),
    path("issues/<int:pk>/return/", views.issue_return, name="issue_return"),
]
