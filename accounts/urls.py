from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.views import IndexView, GoogleLogin, GoogleCallback, GoogleLoginFinish, CreateQRcodeAPIView, VerifyOTPAPIView

app_name = 'accounts'
urlpatterns = [
    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # allauth
    path('allauth/', include('allauth.urls')),
    # simple-jwt
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('index/', IndexView.as_view()),

    # google social login
    path('google/login/', GoogleLogin.as_view()),
    path('google/callback/', GoogleCallback.as_view()),
    path('google/login/finish/', GoogleLoginFinish.as_view()),

    # 2FA - Google OTP
    path('google/otp/', CreateQRcodeAPIView.as_view()),
    path('google/otp/verify/', VerifyOTPAPIView.as_view())

]
