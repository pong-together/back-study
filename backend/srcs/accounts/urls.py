
from django.urls import path, include
from accounts.views import testview

urlpatterns = [
	path("", testview.as_view())
]
