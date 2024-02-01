from django.contrib.auth.models import User
from rest_framework import generics

from users.serializers import SignUpSerializer


# Create your views here.


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer