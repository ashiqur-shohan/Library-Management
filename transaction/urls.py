from django.urls import path
from .views import deposit,UserDepositView

# app_name = 'transactions'
urlpatterns = [
    # path("deposit/", deposit, name="deposit_money"),
    path("deposit/", UserDepositView.as_view(), name="deposit_money"),
]