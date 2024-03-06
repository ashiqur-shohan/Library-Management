from django.contrib import admin
from .models import Transaction
# Register your models here.

# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     def get_name(self, obj):
#         return obj.account.user.first_name()
#     def get_account(self, obj):
#         return obj.account.account_no()
#     list_display = ['account',get_name, 'amount' ]

#     def save_model(self, request, obj, form, change):
#         obj.account.balance += obj.amount
#         obj.account.save()
#         super().save_model(request, obj, form, change)

admin.site.register(Transaction)
