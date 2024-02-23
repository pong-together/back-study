from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.models import ChatRoom, ShopUser, VisitorUser
from chats.serializers import ChatRoomSerializer


# Create your views here.

class ChatRoomListCreateAPIView(APIView):
    def get(self, request):
        try:
            email = request.GET['email']
            chat_rooms = ChatRoom.objects.filter(
                shop_user__shop_user_email=email
            ) | ChatRoom.objects.filter(
                visitor_user__visitor_user_email=email
            )
        except KeyError as e:
            return Response({'error': f'{str(e)} is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        shop_user_email = request.data.get('shop_user_email')
        visitor_user_email = request.data.get('visitor_user_email')

        chatroom = ChatRoom.objects.filter(
            shop_user__shop_user_email=shop_user_email,
            visitor_user__visitor_user_email=visitor_user_email
        )

        if chatroom:
            serializer = ChatRoomSerializer(chatroom, context={'request': self.request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        # 채팅방 생성
        serializer = ChatRoomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        shop_user, _ = ShopUser.objects.get_or_create(shop_user_email=shop_user_email)
        visitor_user, _ = VisitorUser.objects.get_or_create(visitor_user_email=visitor_user_email)
        serializer.save(shop_user=shop_user, visitor_user=visitor_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
