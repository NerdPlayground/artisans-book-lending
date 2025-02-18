from datetime import timedelta
from django.utils import timezone
from appauth.permissions import isOwner
from rest_framework import generics,permissions
from .models import BorrowingRecord
from .serializers import BorrowingRecordSerializer

class BorrowBook(generics.CreateAPIView):
    serializer_class=BorrowingRecordSerializer
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Allows an authenticated user to borrow a book"""
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
            due_on=timezone.now()+timedelta(weeks=2)
        )

class BorrowedBooks(generics.ListAPIView):
    serializer_class=BorrowingRecordSerializer
    permission_classes=[permissions.IsAuthenticated,isOwner]

    def get_queryset(self):
        return BorrowingRecord.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Allows an authenticated user to list their borrowed books"""
        return super().get(request, *args, **kwargs)

class ReturnBook(generics.DestroyAPIView):
    queryset=BorrowingRecord.objects.all()
    serializer_class=BorrowingRecordSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        book=instance.book
        book.available=True
        book.save()
        return super().perform_destroy(instance)

    def destroy(self, request, *args, **kwargs):
        """Allows an authenticated user to return a book"""
        return super().destroy(request, *args, **kwargs)
