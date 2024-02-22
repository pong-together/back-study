from django.urls import path

from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/room/<int:room_id>/messages', ChatConsumer.as_asgi()),
]