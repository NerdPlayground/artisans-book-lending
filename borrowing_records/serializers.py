from books.models import Book
from .models import BorrowingRecord
from rest_framework import serializers

class BorrowingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=BorrowingRecord
        fields=[
            "id","book","user",
            "borrowed_on","due_on",
        ]
        read_only_fields=["user","due_on"]
    
    def create(self, validated_data):
        book_id=validated_data.get("book")
        book=Book.objects.get(id=book_id)
        book.available=False
        book.save()
        return super().create(validated_data)
