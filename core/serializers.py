from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField
from django_rest_framework_base64_fields.fields import Base64FileField
from drf_extra_fields.fields import Base64ImageField


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')
    image = Base64ImageField(max_length=None, use_url=True,required=False,allow_null=True,)
    file= Base64FileField(required=False,allow_null=True,)

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            img = validated_data.get('image')
        except:
            img = None
        
        try:
            file = validated_data.get('file')
        except:
            file = None

        body=validated_data.get('body')

        recipient = get_object_or_404(User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=body,
                           image=img,
                           file=file,
                           user=user,
                           is_read= False)
        
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'image', 'file', 'is_read')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
