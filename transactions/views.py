from functools import partial
from xml.dom import ValidationErr
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Transaction
from .serializers import TransactionSerializer
from authapi.models import Customer
from authapi.serializers import UserSerializer
from django.db.models import Q


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

class TransactionList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    #get a logged in account transactions
    def get(self, request):
        
        try :
            transactions = Transaction.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
            serializer = TransactionSerializer(transactions, many=True)
        except TypeError:
            return Response({"error":"Type error occured"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ValidationErr:
            return Response({"error":"Could not validate your request"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):

        try :
            if 'amount_to_send' not in request.data and isinstance(request.data['amount_to_send'], int) :
                return Response({"error":"amount is required and has to be a number"}, status=status.HTTP_403_FORBIDDEN)

            if request.data and 'receiver' not in request.data:
                return Response({"error":"You need an account to send to"}, status=status.HTTP_403_FORBIDDEN)

            if request.user.account_number != request.data['sender']:
                return Response({"error":"Please put your account number as the sender"}, status=status.HTTP_403_FORBIDDEN)

            if request.data['sender'] == request.data['receiver']:
                return Response({"error":"Please, you can only send to other accounts"}, status=status.HTTP_403_FORBIDDEN)
            if request.user.account_balance < request.data['amount_to_send']:
                return Response({"error":"Insufficient balance"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            #validate receiver
            receiver = Customer.objects.get(account_number=request.data['receiver'])
            sender = Customer.objects.get(account_number=request.data['sender'])

            request.data['receiver'] = receiver.id
            request.data['sender'] = sender.id
            request.data['amount'] = request.data.get('amount_to_send')
            if not receiver:
                return Response({"error":"receiver is not recognised"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TransactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                receiver.account_balance += float(request.data['amount'])
                receiver.save()
                sender.account_balance -= float(request.data['amount'])
                sender.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response({"error":"Type error occured"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ValidationErr:
            return Response({"error":"Could not validate your request"}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as e:
            raise e

class FundWalletView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request):
        try:
            customer = Customer.objects.get(pk=request.user.id)
            return customer
        except Customer.DoesNotExist:
            return None

    def get(self, request):
        customer_instance = self.get_object(request)
        if not customer_instance:
            return Response({"res":"Object with id doest exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "balance":customer_instance.account_balance,
                "account_number":customer_instance.account_number,
                "phone_number":customer_instance.phone_number,
                "Name":customer_instance.first_name+' '+customer_instance.last_name
            }, 
            status=status.HTTP_200_OK
        )

    def patch(self, request):

        if isinstance(request.data['amount'], float) and request.data['amount'] > 0:
            customer_instance = self.get_object(request)
            if not customer_instance:
                return Response({"res":"Object with id doest exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            new_balance = customer_instance.account_balance + request.data.get('amount')
            data = {
                "account_balance" : new_balance
            }
            serializer =  UserSerializer(instance=customer_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Amount is required and should be a number"}, status=status.HTTP_400_BAD_REQUEST)