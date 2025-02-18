from books.models import Book
from .models import BorrowingRecord
from rest_framework import serializers
from books.serializers import BookSerializer
from profiles.serializers import UserSerializer

class BorrowingRecordSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    book=BookSerializer()

    class Meta:
        model=BorrowingRecord
        fields=["id","book","user"]
    
    def create(self, validated_data):
        book_id=validated_data.get("book")
        book=Book.objects.get(id=book_id)
        book.available=False
        book.save()
        return super().create(validated_data)
