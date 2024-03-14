from django.urls import path
from .views import UserDepositView

# app_name = 'transactions'
urlpatterns = [
    path("deposit/", UserDepositView.as_view(), name="deposit_money"),
]