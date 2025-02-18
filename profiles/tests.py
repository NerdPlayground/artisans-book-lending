import re
from .models import Profile
from django.urls import reverse
from pocket.tests import PocketTestCase

class ProfileTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def access_all_users(self,actor):
        token=self.member_login(actor)
        count=Profile.objects.count()
        response=self.client.get(
            path=reverse("user-list"),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response,count

    def test_admin_access_all_users(self):
        response,count=self.access_all_users(self.admin)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),count)
    
    def test_member_access_all_users(self):
        response,count=self.access_all_users(self.member)
        self.assertEqual(response.status_code,403)
    
    def test_member_search_for_user(self):
        token=self.member_login(self.member)
        username=self.intruder.user.username
        response=self.client.get(
            path=reverse("user-detail",kwargs={"username":username}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(username,response.json().get("username"))
