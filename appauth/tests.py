import re
from django.core import mail
from django.urls import reverse
from knox.models import AuthToken
from profiles.models import Profile
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

class AppAuthTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def verify_user_email(self,username):
        pattern="key: (?P<key>[-:\w]+)"
        key=re.search(pattern,mail.outbox[0].body).group("key")
        response=self.client.post(
            path=reverse("rest_verify_email"),
            data={"key":key}
        )
        self.assertEqual(response.status_code,200)

        current_user=get_user_model().objects.get(username=username)
        email_address=EmailAddress.objects.get(user=current_user)
        self.assertTrue(email_address.verified)

    def setup_profile_details(self,token,details):
        response=self.client.put(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
            content_type="application/json",
            data=details,
        )
        self.assertEqual(response.status_code,200)

    def test_member_registration(self):
        details={
            "username":"johndoe",
            "email":"johndoe@gmail.com",
            "first_name":"John",
            "last_name":"Doe",
            # add profile information
            # profile:{"field":"value"}
        }
        response=self.client.post(reverse("rest_register"),{
            "username":details.get("username"),
            "email":details.get("email"),
            "password1":self.password,
            "password2":self.password,
        })
        self.assertEqual(response.status_code,204)
        self.assertEqual(len(mail.outbox),1)
        self.verify_user_email(details.get("username"))

        profile=Profile.objects.last()
        token=self.member_login(profile,self.password)
        self.setup_profile_details(token,details)

        profile=Profile.objects.last()
        self.assertEqual(profile.user.username,details.get("username"))
        self.assertEqual(profile.user.email,details.get("email"))
        self.assertEqual(profile.user.first_name,details.get("first_name"))
        self.assertEqual(profile.user.last_name,details.get("last_name"))
        # check profile information
    
    def test_member_delete_account(self):
        token=self.member_login(self.dummy)
        total_members=Profile.objects.count()
        response=self.client.delete(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(Profile.objects.count(),total_members-1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def test_member_change_password(self):
        token=self.member_login(self.member)
        password="QWERTY123!@#"
        response=self.client.post(
            headers={"Authorization": f"Bearer {token}"},
            path=reverse("rest_password_change"),
            data={
                "old_password":self.password,
                "new_password1":password,
                "new_password2":password,
            }
        )
        self.assertEqual(response.status_code,200)

        logout_response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(logout_response.status_code,204)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)
    
    def test_member_password_reset(self):
        response=self.client.post(
            path=reverse("password_reset:reset-password-request"),
            data={"email":self.member.user.email},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(mail.outbox),1)

        pattern="Authentication Token: (?P<token>[\w]+)"
        token=re.search(pattern,mail.outbox[0].body).group("token")
        token_response=self.client.post(
            path=reverse("password_reset:reset-password-validate"),
            data={"token":token}
        )
        self.assertEqual(token_response.status_code,200)

        password="QWERTY23!@#"
        reset_response=self.client.post(
            path=reverse("password_reset:reset-password-confirm"),
            data={"token":token,"password":password,}
        )
        self.assertEqual(reset_response.status_code,200)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)
    
    def test_member_logout(self):
        token_counter=AuthToken.objects.count()
        token=self.member_login(self.member)
        self.assertEqual(AuthToken.objects.count(),token_counter+1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(AuthToken.objects.count(),token_counter)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def test_member_logout_all_sessions(self):
        token_counter=AuthToken.objects.filter(user=self.member.user).count()
        all_tokens=AuthToken.objects.count()
        token=self.member_login(self.member)
        self.assertEqual(AuthToken.objects.count(),token_counter+1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(
            path=reverse("knox_logout_all"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(AuthToken.objects.count(),all_tokens-token_counter)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
