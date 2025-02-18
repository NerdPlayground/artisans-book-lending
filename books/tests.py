from .models import Book
from random import choice
from django.urls import reverse
from pocket.tests import PocketTestCase

class BookTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def add_book(self,actor):
        token=self.member_login(actor)
        count=Book.objects.count()
        data={
            "isbn":"978-1-04-876475-0",
            "title":"Endless",
            "author":"George Mobisa",
        }
        response=self.client.post(
            path=reverse("add-book"),
            headers={"Authorization":f"Bearer {token}"},
            data=data,
        )
        return response,count,data
    
    def test_member_add_book(self):
        response,count,data=self.add_book(self.admin)
        self.assertEqual(response.status_code,201)
        self.assertEqual(Book.objects.count(),count+1)

        book=Book.objects.first()
        self.assertEqual(book.isbn,data.get("isbn"))
        self.assertEqual(book.title,data.get("title"))
        self.assertEqual(book.author,data.get("author"))
    
    def test_admin_add_book(self):
        response,count,data=self.add_book(self.member)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Book.objects.count(),count)
    
    def list_books(self,actor=None):
        headers=None
        if actor:
            token=self.member_login(actor)
            headers={"Authorization":f"Bearer {token}"}
        
        count=Book.objects.count()
        response=self.client.get(
            path=reverse("book-list"),
            headers=headers,
        )
        return response,count
    
    def test_authenticated_user_list_books(self):
        response,count=self.list_books(self.member)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),count)
    
    def test_unauthenticated_user_list_books(self):
        response,count=self.list_books()
        self.assertEqual(response.status_code,401)
    
    def check_book_details(self,book,data):
        self.assertEqual(str(book.id),data.get("id"))
        self.assertEqual(book.isbn,data.get("isbn"))
        self.assertEqual(book.title,data.get("title"))
        self.assertEqual(book.author,data.get("author"))
    
    def get_book(self,actor=None):
        headers=None
        if actor:
            token=self.member_login(actor)
            headers={"Authorization":f"Bearer {token}"}
        
        book=choice(self.books)
        response=self.client.get(
            path=reverse("book-detail",kwargs={"pk":book.id}),
            headers=headers,
        )
        return response,book

    def test_authenticated_user_get_book(self):
        response,book=self.get_book(self.member)
        self.assertEqual(response.status_code,200)

        data=response.json()
        self.check_book_details(book,data)

    def test_unauthenticated_user_get_book(self):
        response,book=self.get_book()
        self.assertEqual(response.status_code,401)
    
    def edit_book(self,actor):
        token=self.member_login(actor)
        book=choice(self.books)
        data={
            "isbn":book.isbn,
            "title":"Endless: Book 1",
            "author":book.author,
        }
        response=self.client.put(
            path=reverse("edit-book",kwargs={"pk":book.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        book.refresh_from_db()
        return response,book,data
    
    def test_admin_edit_book(self):
        response,book,data=self.edit_book(self.admin)
        self.assertEquals(response.status_code,200)

        data=response.json()
        self.check_book_details(book,data)
    
    def test_member_edit_book(self):
        response,book,data=self.edit_book(self.member)
        self.assertEquals(response.status_code,403)
    
    def delete_book(self,actor):
        token=self.member_login(actor)
        book=choice(self.books)
        count=Book.objects.count()
        response=self.client.delete(
            path=reverse("edit-book",kwargs={"pk":book.id}),
            headers={"Authorization":f"Bearer {token}"},
        )
        return response,count
    
    def test_admin_delete_book(self):
        response,count=self.delete_book(self.admin)
        self.assertEqual(response.status_code,204)
        self.assertEqual(Book.objects.count(),count-1)
    
    def test_member_delete_book(self):
        response,count=self.delete_book(self.member)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Book.objects.count(),count)
