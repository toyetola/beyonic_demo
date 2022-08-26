from django.contrib.auth.models import User
from .models import Customer
from rest_framework import serializers
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email", "phone_number", "password", "account_number", "account_balance", "created", "updated"]
        extra_kwargs = {'password': {'write_only': True}}

    