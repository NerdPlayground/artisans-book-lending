from django.urls import path
from .views import AddBook,BookDetail,BookList,BookEdit

urlpatterns=[
    path("add/",AddBook.as_view(),name="add-book"),
    path("",BookList.as_view(),name="book-list"),
    path("<str:pk>/",BookDetail.as_view(),name="book-detail"),
    path("<str:pk>/edit/",BookEdit.as_view(),name="edit-book"),
]
