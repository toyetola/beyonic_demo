from django.test import TestCase

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from authapi.models import Customer
from transactions.models import Transaction
from authapi.serializers import UserSerializer
from authapi.tests import AccountTests





class TransactionTests(APITestCase, URLPatternsTestCase):

    def create_a_transaction(self):

        user = Customer.objects.get(email='test-email2@gmail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse('create-transaction')

        data = {
            "sender":AccountTests.user1['account_number'],
            "receiver":AccountTests.user2['account_number'],
            "amount_to_send":5000.00
        }
        transaction = Transaction.objects.all()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data, transaction[0])