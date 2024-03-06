from django.contrib import admin
from .models import UserAccount,BorrowHistory
# Register your models here.

admin.site.register(UserAccount)
admin.site.register(BorrowHistory)