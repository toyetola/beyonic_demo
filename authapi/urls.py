from distutils.log import Log
from importlib.resources import path
from .views import RegisterView, LoginView, LogoutView, index
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='customer-login'),
    path('logout/', LogoutView.as_view(), name='customer-logout'),
]