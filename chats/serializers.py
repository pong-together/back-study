from rest_framework import serializers

from chats.models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'room', 'sender_email', 'text', 'timestamp', )


class ChatRoomSerializer(serializers.ModelSerializer):
    shop_user_email = serializers.SerializerMethodField()
    visitor_user_email = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('id', 'shop_user_email', 'visitor_user_email', 'messages')

    def get_shop_user_email(self, obj):
        return obj.shop_user.shop_user_email

    def get_visitor_user_email(self, obj):
        return obj.visitor_user.visitor_user_email