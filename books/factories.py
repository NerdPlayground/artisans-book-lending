import factory
from .models import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Book
    
    isbn=factory.Faker("isbn13")
    title=factory.Faker("sentence",nb_words=4)
    author=factory.Faker("name")
