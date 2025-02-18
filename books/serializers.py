from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[
            "id","isbn","title","author",
            "available","created_at",
        ]
