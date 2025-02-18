from django.urls import path
from .views import BorrowBook,ReturnBook,BorrowedBooks

urlpatterns=[
    path("",BorrowedBooks.as_view(),name="borrowed-books"),
    path("borrow-book/",BorrowBook.as_view(),name="borrow-book"),
    path("return-book/",ReturnBook.as_view(),name="return-book"),
]
