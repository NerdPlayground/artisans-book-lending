from .models import Book
from django.contrib import admin

class BookAdmin(admin.ModelAdmin):
    list_display=[
        "isbn","title","author",
        "available","created_at",
    ]
    search_fields=[
        "isbn","title","author",
    ]
    list_filter=[
        "author","available",
    ]

admin.site.register(Book, BookAdmin)
