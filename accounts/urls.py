from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.views import IndexView

app_name = 'accounts'
urlpatterns = [
    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # allauth
    path('allauth/', include('allauth.urls')),

    path('index/', IndexView.as_view())
]
