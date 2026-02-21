from django import forms
from .models import Book, Reader, BookLoan


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "year")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Автор"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Год", "min": 1}),
        }


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ("name", "email", "phone")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "ФИО"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
        }


class IssueBookForm(forms.ModelForm):
    class Meta:
        model = BookLoan
        fields = ("book", "reader")
        widgets = {
            "book": forms.Select(attrs={"class": "form-select"}),
            "reader": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Book, BookLoan, Reader
        issued_book_ids = BookLoan.objects.filter(returned_at__isnull=True).values_list("book_id", flat=True)
        self.fields["book"].queryset = Book.objects.exclude(id__in=issued_book_ids)
        self.fields["reader"].queryset = Reader.objects.all().order_by("name")
