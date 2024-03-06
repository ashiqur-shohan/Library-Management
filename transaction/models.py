from django.db import models
from user.models import UserAccount
# Create your models here.
TRANSACTION_TYPE = (
    ('Deposite', 'Deposite'),
    ('Borrow', 'Borrow'),
)
class Transaction(models.Model):
    # account = models.ForeignKey(UserAccount, related_name = 'transactions', on_delete = models.CASCADE) 
    # amount = models.DecimalField(decimal_places=2, max_digits = 12)
    # transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    
    account = models.ForeignKey(UserAccount, on_delete = models.CASCADE, related_name = 'accounts')
    amount = models.DecimalField(max_digits = 12, decimal_places = 2)
    timestamp = models.DateTimeField(auto_now_add = True,null = True)
    
 
    