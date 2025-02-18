from .models import Book
from .serializers import BookSerializer
from rest_framework import generics,permissions

class AddBook(generics.CreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        """Allows admin to add a book to the library"""
        return super().post(request, *args, **kwargs)

class BookList(generics.ListAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Allows authenticated users to list available books"""
        return super().get(request, *args, **kwargs)

class BookDetail(generics.RetrieveAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Allows authenticated users to get a book's details"""
        return super().get(request, *args, **kwargs)

class BookEdit(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        """Allows admin to partially update a book's details"""
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Allows admin to update a book's details"""
        return super().patch(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Allows admin to remove a book from the library"""
        return super().destroy(request, *args, **kwargs)
