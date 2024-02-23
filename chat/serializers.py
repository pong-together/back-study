from rest_framework import serializers

from chat.models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    opponent_email = serializers.SerializerMethodField()
    shop_user_email = serializers.SerializerMethodField()
    visitor_user_email = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True, source="messages.all")

    class Meta:
        model = ChatRoom
        fields = ('id', 'shop_user_email', 'visitor_user_email', 'latest_message', 'opponent_email', 'messages')

    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(room=obj).order_by('-timestamp').first()
        if latest_msg:
            return latest_msg.text
        return None

    def get_opponent_email(self, obj):
        request_user_email = self.context['request'].query_params.get('email', None)

        if request_user_email == obj.shop_user.shop_user_email:
            return obj.visitor_user.visitor_user_email
        else:
            return obj.shop_user.shop_user_email

    def get_shop_user_email(self, obj):
        return obj.shop_user.shop_user_email

    def get_visitor_user_email(self, obj):
        return obj.visitor_user.visitor_user_email
