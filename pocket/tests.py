from random import choice
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from profiles.factories import ProfileFactory
from books.factories import BookFactory
from borrowing_records.factories import BorrowingRecordsFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="A!q2L#w4S$o6K&p8"
        cls.admin=ProfileFactory.create(user__is_staff=True)
        cls.member,cls.intruder,cls.dummy=ProfileFactory.create_batch(3)

        cls.books=BookFactory.create_batch(20)
        cls.borrowing_record=BorrowingRecordsFactory.create(
            user=cls.member.user,book=cls.books[0],
            due_on=timezone.now()+timedelta(weeks=2)
        )
        cls.books[0].available=False
        cls.books[0].save()

    def member_login(self,member,password=None):
        password=password or self.password
        response=self.client.post(reverse("knox_login"),{
            "password":password,
            "username":member.user.username,
        })
        self.assertEqual(response.status_code,200)
        return response.json().get("token")

    def get_current_user(self,token):
        response=self.client.get(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response
