from http.client import HTTPException
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions

from .models import Customer
from .serializers import UserSerializer
from random import randint

def generateRandomNumber(n):
    return ''.join(["{}".format(randint(0, 9)) for _ in range(n)])


def index(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        print(request.data)

        try:
            country_codes_accepted = ['+234', '+256']


            if 'phone_number' not in request.data:
                return Response({"error":"phone number is required"}, status=status.HTTP_403_FORBIDDEN)

            if request.data['phone_number'][:4] not in country_codes_accepted :
                return Response({"error":"phone number should have country codes accepted"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if len(request.data['phone_number']) != 14 :
                return Response({"error":"phone number too short or longer than it should"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            account_number = generateRandomNumber(10)
            request.data['account_number'] = account_number
            print(request.data)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__)
            raise e
        

class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        try:
            username = ""
            if request.data.get("email") :
                username = request.data.get("email")
            elif 'phone_number' in request.data:
                username = request.data.get("email")
            password = request.data.get("password")
            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'}, status=status.HTTP_401_UNAUTHORIZED)

            if request.data.get("email") :
                user = Customer.objects.get(email=username)
            else:
                user = Customer.objects.get(phone_number=username)

            if not user:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            token, _ = Token.objects.get_or_create(user=user)
            # print(type(token.user.email))
            return Response({'token': token.key, 'email':token.user.email, 'account_number':token.user.account_number}, status=status.HTTP_200_OK)
        
        except Customer.DoesNotExist:
            return Response({"error":"user does not exit"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            raise ex


class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"message":"successfully logged out"},status=status.HTTP_200_OK)
