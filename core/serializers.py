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

    def create(self, validated_data):
        user = self.context["request"].user
        room = validated_data["group"]  # but why does this return THE room?
        msg = MessageModel(
            group=room,
            user=user,
            body=validated_data["body"],
        )
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ("id", "user", "group", "timestamp", "body")


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class RoomModelSerializer(ModelSerializer):
    class Meta:
        model = RoomModel
        fields = "__all__"
