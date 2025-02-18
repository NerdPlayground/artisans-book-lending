from random import choice
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from pocket.tests import PocketTestCase
from borrowing_records.models import BorrowingRecord

class BorrowingRecordsTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def borrow_book(self,book,actor=None):
        headers=None
        if actor:
            token=self.member_login(actor)
            headers={"Authorization":f"Bearer {token}"}
        
        data={"book":book.id}
        response=self.client.post(
            path=reverse("borrow-book"),
            headers=headers,
            data=data,
        )
        book.refresh_from_db()
        return response

    def test_authenticated_user_borrow_book(self):
        book=choice(self.books[1:])
        response=self.borrow_book(book,self.member)
        self.assertEqual(response.status_code,201)

        date_time_format="%Y-%m-%d %H:%M:%S %Z"
        record=BorrowingRecord.objects.first()
        self.assertEqual(record.book,book)
        self.assertEqual(record.user,self.member.user)
        self.assertFalse(record.book.available)
        self.assertEqual(
            record.due_on.strftime(date_time_format),
            (timezone.now()+timedelta(weeks=2)).strftime(date_time_format)
        )
    
    def test_unauthenticated_user_borrow_book(self):
        book=choice(self.books[1:])
        response=self.borrow_book(book)
        self.assertEqual(response.status_code,401)
        self.assertTrue(book.available)
    
    def test_authenticated_user_borrow_unavailable_book(self):
        book=self.books[0]
        response=self.borrow_book(book,self.member)
        self.assertEqual(response.status_code,400)
        self.assertFalse(book.available)
    
    def return_book(self,actor=None):
        headers=None
        if actor:
            token=self.member_login(actor)
            headers={"Authorization":f"Bearer {token}"}
        
        book=self.borrowing_record.book
        response=self.client.delete(
            path=reverse("return-book",
                kwargs={"pk":self.borrowing_record.id}
            ),
            headers=headers,
        )
        book.refresh_from_db()
        return response,book

    def test_authenticated_user_return_book(self,actor=None):
        response,book=self.return_book(self.member)
        self.assertEqual(response.status_code,204)
        self.assertTrue(book.available)
    
    def test_unauthenticated_user_return_book(self,actor=None):
        response,book=self.return_book()
        self.assertEqual(response.status_code,401)
    
    def list_borrowed_books(self,actor=None):
        count=0
        headers=None
        if actor:
            token=self.member_login(actor)
            headers={"Authorization":f"Bearer {token}"}
            count=BorrowingRecord.objects.filter(user=actor.user).count()
        
        response=self.client.get(
            path=reverse("borrowed-books"),
            headers=headers,
        )
        return response,count

    def test_authenticated_user_list_borrowed_books(self):
        response,count=self.list_borrowed_books(self.member)
        self.assertEqual(response.status_code,200)
        self.assertEqual(count,len(response.json()))
    
    def test_unauthenticated_user_list_borrowed_books(self):
        response,count=self.list_borrowed_books()
        self.assertEqual(response.status_code,401)
        self.assertEqual(count,0)
