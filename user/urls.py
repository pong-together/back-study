from django.urls import path, include

import user
from user.views import RegisterAPIView

urlpatterns = [
    path('user/register/', RegisterAPIView.as_view()),
]