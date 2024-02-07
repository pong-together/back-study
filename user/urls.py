from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import user
from user.views import MypageAPIView, MyTokenObtainPairView

urlpatterns = [

    path('dj-rest-auth/', include('dj_rest_auth.urls')), #다양한 url 제공
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), #registration url 제공

    path('api/token/', TokenObtainPairView.as_view()), #로그인 정보 받고 accessToken, refreshToken 발급
    path('api/token/login/', MyTokenObtainPairView.as_view()), #위에 뷰 커스터마이징 해줌
    path('api/token/refresh/', TokenRefreshView.as_view()), #refresToken 정보 받고, accessToken 발급


    path('mypage/<int:id>/', MypageAPIView.as_view()),

    #path('api/user/', include('allauth.urls')),
]