from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user=models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )
    banned=models.BooleanField(default=False)
