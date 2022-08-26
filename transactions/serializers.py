from rest_framework import serializers

from authapi.models import Customer
from authapi.serializers import UserSerializer
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    your_balance = serializers.ReadOnlyField(source='sender.account_balance')
    
    class Meta:
        model = Transaction
        fields = ['sender', 'receiver', 'amount', 'created', 'updated', 'your_balance']