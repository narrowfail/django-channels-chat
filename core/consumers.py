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
            async_to_sync(self.channel_layer.group_add)(
                group.name,
                self.channel_name,
            )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]
        recipient_group = text_data_json["room_name"]
        message_text = text_data_json["message"]

        if message_type == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
                recipient_group,
                {
                    "type": "chat_message",
                    "message": f"New Message @ {recipient_group}: {message_text}",
                },
            )

    def notify_new_msg(self, msg):
        """
        Sends notification to all listening WS clients belonging to this msg (MessageModel).
        """
        send_to_group = msg.group.name
        send_msg = {
            "type": "chat_message",
            "message": msg.body,
        }
        async_to_sync(self.channel_layer.group_send)(
            send_to_group,
            send_msg,
        )

    def chat_message(self, event):
        """
        Handler for 'chat_message' type of WS messages
        """
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def connection_message(self, event):
        """
        Handler for verbose messages
        """
        message = event["message"]
        print("WS: " + message)

    @staticmethod
    def fetch_user_groups(user):
        user_groups = RoomModel.objects.filter(members__username=user)
        return user_groups
