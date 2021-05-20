from django.contrib.admin import ModelAdmin, site
from core.models import MessageModel, RoomModel


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ("timestamp",)
    search_fields = ("id", "body", "user__username", "recipient__username")
    list_display = ("id", "user", "recipient", "timestamp", "characters")
    list_display_links = ("id",)
    list_filter = ("user", "recipient")
    date_hierarchy = "timestamp"


class RoomModelAdmin(ModelAdmin):
    list_display = (
        "group",
        # "members",
    )


site.register(MessageModel, MessageModelAdmin)
site.register(RoomModel, RoomModelAdmin)
