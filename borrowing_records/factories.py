import factory
from .models import BorrowingRecord
from books.factories import BookFactory
from profiles.factories import ProfileFactory

class BorrowingRecordsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=BorrowingRecord
    
    book=factory.SubFactory(BookFactory)
    user=factory.SubFactory(ProfileFactory)
