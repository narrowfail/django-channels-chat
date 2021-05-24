from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import RoomModel
import json


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None

    def connect(self):
        self.username = self.scope["user"].username

        for group in self.fetch_user_groups(self.username):
            async_to_sync(self.channel_layer.group_add)(group.name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        recipient_group = text_data_json["room_name"]

        async_to_sync(self.channel_layer.group_send)(
            recipient_group,
            {
                "type": "chat_message",
                "message": "test message. ",
            },
        )

    # Handler for 'chat_message' type of WS messages
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    @staticmethod
    def fetch_user_groups(user):
        user_groups = RoomModel.objects.filter(members__username=user)
        return user_groups
