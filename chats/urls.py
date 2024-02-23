from django.urls import path

from chats.views import ChatRoomListCreateAPIView

app_name = 'chats'
urlpatterns = [
    path('rooms/', ChatRoomListCreateAPIView.as_view(), name='chat_rooms'),
]