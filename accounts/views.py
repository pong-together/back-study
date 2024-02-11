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
    def get(self, request):
        scope = "https://www.googleapis.com/auth/userinfo.email"
        client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
        return redirect(
            f"{AUTH_URI}?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


class GoogleCallback(APIView):
    def get(self, request):
        client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
        authorization_code = request.GET.get("code")

        # 1. resource server에 access token 요청
        token_request = requests.post(
            f"{TOKEN_URI}?client_id={client_id}&client_secret={client_secret}&code={authorization_code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")

        token_json_request = token_request.json()
        error = token_json_request.get("error")

        if error is not None:
            raise JSONDecodeError(error)

        access_token = token_json_request.get("access_token")

        # 2. access token으로 API 호출 - email 가져오기
        headers = {'Authorization': f'Bearer {access_token}'}

        email_request = requests.get(f'{USERINFO_URI}', headers=headers)

        if email_request.status_code != 200:
            return JsonResponse({'error_message': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

        email_json_request = email_request.json()
        email = email_json_request.get('email')

        # 3. email에 매칭되는 user의 jwt 발급
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user_by_oauth(email=email)
        finally:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            token_response = {
                'access_token': access_token,
                'refresh_token': str(refresh),
            }
        return Response(token_response, status=status.HTTP_200_OK)
