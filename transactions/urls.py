from .views import TransactionList, FundWalletView
from django.urls import path

urlpatterns = [
    path('transact/', TransactionList.as_view(), name='create-transaction'),
    path('fundWallet/', FundWalletView.as_view(), name='fund-wallet')
]