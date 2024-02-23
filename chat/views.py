from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from chat.models import ChatRoom, ShopUser, VisitorUser
from chat.serializers import ChatRoomSerializer


# Create your views here.


class ImmediateResponseException(Exception):
    def __init__(self, response):
        self.response = response


class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
            user_email = self.request.query_params.get('email', None)

            if not user_email:
                raise ValidationError('Email 파라미터가 필요합니다.')

            return ChatRoom.objects.filter(
                shop_user__shop_user_email=user_email
            ) | ChatRoom.objects.filter(
                visitor_user__visitor_user_email=user_email
            )
        # except ValidationError as e:
        #     content = {'detail': e.detail}
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     content = {'detail': str(e)}
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    def get_serializer_context(self):
        context = super(ChatRoomListCreateView, self).get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ImmediateResponseException as e:
            return e.response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        shop_user_email = self.request.data.get('shop_user_email')
        visitor_user_email = self.request.data.get('visit_user_email')

        shop_user, _ = ShopUser.objects.get_or_create(shop_user_email=shop_user_email)
        visitor_user, _ = VisitorUser.objects.get_or_create(visitor_user_email=visitor_user_email)

        existing_chatroom = ChatRoom.objects.filter(shop_user__shop_user_email=shop_user_email,
                                                    visitor_user__visitor_user_email=visitor_user_email).first()
        if existing_chatroom:
            serializer = ChatRoomSerializer(existing_chatroom, context={'request': self.request})
            raise ImmediateResponseException(Response(serializer.data, status=status.HTTP_200_OK))
        serializer.save(shop_user=shop_user, visitor_user=visitor_user)