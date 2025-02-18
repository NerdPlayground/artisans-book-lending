import uuid
from django.db import models
from django.contrib.auth import get_user_model

class BorrowingRecord(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    book=models.OneToOneField(
        "books.Book",
        related_name="borrowing_record",
        on_delete=models.CASCADE,
    )
    user=models.ForeignKey(
        get_user_model(),
        related_name="borrowing_records",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} borrowed {self.book}"
