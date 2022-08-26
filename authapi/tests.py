from django.test import TestCase
from rest_framework.test import APIRequestFactory

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from authapi.models import Customer
from transactions.models import Transaction
from authapi.serializers import UserSerializer


class AccountTests(APITestCase, URLPatternsTestCase):

    user1 = None
    user2  = None
    
    urlpatterns = [
        path('api/', include('authapi.urls')),
    ]

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """

        url = reverse('customer-register')

        data = [
            {
                "email":"test-email2@gmail.com",
                "first_name":"Test2",
                "last_name":"User2",
                "password":"12345678",
                "phone_number":"+2348123443502"
            },
            {
                
                "email":"test-email1@gmail.com",
                "first_name":"Test1",
                "last_name":"User1",
                "password":"12345678",
                "phone_number":"+2347304435003"
            }
        ]
        count = 0
        for d in data:
            response = self.client.post(url, d, format='json')
            count += 1
            if count == 1:
                self.user1 = response
            elif count == 2:
                self.user2 = response

        customer = Customer.objects.count()
        print(customer)
        serializer = UserSerializer(customer)
        self.assertEqual(customer, 2)


    """ def test_login(self):
        \"""
        Ascertain login
        \"""

        url = reverse('customer-login')

        data = {
            "email":"test-email2@gmail.com",
            "password":"12345678",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) """


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
        response = client.post(url, data, format='json')
        self.assertEqual(response.data, transaction[0])

    


        

    

    