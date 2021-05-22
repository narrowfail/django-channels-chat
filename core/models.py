from django.contrib.auth.models import User, Group
from django.db.models import (
    Model,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    OneToOneField,
    ManyToManyField,
    CharField,
)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class RoomModel(Model):
    """
    Do NOT extend auth.models.Group as a "Room Group" model
    unless you want to spend another 3 hour meaninglessly
    debugging like me.
    """
    base_group = OneToOneField(
        Group,
        related_name="room_group",
        on_delete=CASCADE,
        parent_link=True,
    )

    members = ManyToManyField(
        User,
        related_name="room_member",
    )

    title = CharField(default="", max_length=50)


class MessageModel(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name="user",
        related_name="from_user",
        db_index=True,
    )
    group = ForeignKey(
        RoomModel,
        on_delete=CASCADE,
        related_name="message_group",
    )

    timestamp = DateTimeField(
        "timestamp", auto_now_add=True, editable=False, db_index=True
    )
    body = TextField("body")

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            "type": "recieve_group_message",
            "message": "{}".format(self.id),
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        # print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        # async_to_sync(channel_layer.group_send)(
        #     "{}".format(self.recipient.id), notification
        # )

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = "core"
        verbose_name = "message"
        verbose_name_plural = "messages"
        ordering = ("-timestamp",)
