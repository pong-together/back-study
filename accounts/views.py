import os
import requests

from django.http import JsonResponse
from django.shortcuts import redirect
from requests import JSONDecodeError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


# Create your views here.

class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


state = os.environ.get("STATE")
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
USERINFO_URI = "https://www.googleapis.com/oauth2/v1/tokeninfo"


class GoogleLogin(APIView):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

    def get(self, request):
        return redirect(
            f"{AUTH_URI}?client_id={self.client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={self.scope}")


class GoogleCallback(APIView):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")

    def get(self, request):
        authorization_code = request.GET.get("code")
        access_token = self.get_access_token(authorization_code)
        email = self.get_email(access_token)

        if email is None:
            return JsonResponse({'error_message': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. email에 매칭되는 user의 jwt 발급
        user = self.get_user(email)
        refresh = RefreshToken.for_user(user)
        response = redirect(BASE_URL + "accounts/google/login/finish/")
        response.set_cookie("access_token", str(refresh.access_token))
        response.set_cookie("refresh_token", str(refresh))
        return response

    def get_access_token(self, authorization_code):
        # 1. resource server에 access token 요청
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_CALLBACK_URI,
            "state": state
        }
        token_response = requests.post(TOKEN_URI, data=data).json()
        error = token_response.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        access_token = token_response.get("access_token")
        return access_token

    def get_email(self, access_token):
        # 2. access token으로 API 호출 - email 가져오기
        headers = {'Authorization': f'Bearer {access_token}'}
        email_response = requests.get(f'{USERINFO_URI}', headers=headers)
        if email_response.status_code != 200:
            return None
        return email_response.json().get('email')

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user_by_oauth(email=email)
        return user


class GoogleLoginFinish(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)
