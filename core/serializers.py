from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import MessageModel, RoomModel
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    PrimaryKeyRelatedField,
)


class MessageModelSerializer(ModelSerializer):
    user = CharField(source="user.username", read_only=True)
    recipient = CharField(source="recipient.username")
    group = CharField()

    def create(self, validated_data):
        user = self.context["request"].user
        recipient = get_object_or_404(
            User, username=validated_data["recipient"]["username"]
        )
        group = get_object_or_404(
            RoomModel, id=validated_data["recipient"]
        )
        msg = MessageModel(recipient=recipient, group=group, body=validated_data["body"],
                           user=user, )
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ("id", "user", "recipient", "group", "timestamp", "body")


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class RoomModelSerializer(ModelSerializer):
    class Meta:
        model = RoomModel
        fields = "__all__"
