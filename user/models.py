from django.db import models
from django.contrib.auth.models import User
from .constants import  GENDER_TYPE
from book.models import BookModel

# Create your models here.
 

class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name='account', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    birth_date = models.DateField(null=True, blank=True)
    mobile_no = models.IntegerField()
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} "

class BorrowHistory(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='borrow_history')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE,related_name='borrow_history')
    borrow_date = models.DateField(auto_now_add=True)
