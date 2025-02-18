import uuid
from django.db import models

class Book(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    isbn=models.CharField(max_length=17,unique=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author}"
