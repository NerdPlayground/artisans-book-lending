from django.contrib import admin
from .models import BorrowingRecord

class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display=[
        "id","book","user",
        "borrowed_on","due_on",
    ]
    search_fields=[
        "book","user",
    ]
    list_filter=[
        "book","user",
    ]

    def has_add_permission(self,request):
        return False

    def has_change_permission(self,request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

admin.site.register(BorrowingRecord,BorrowingRecordAdmin)
