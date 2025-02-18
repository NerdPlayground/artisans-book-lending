from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user=models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )

    # Django's built-in user model is retained for authentication 
    # add extra fields here and ensure they are either nullable or with defaults
