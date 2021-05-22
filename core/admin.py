from django.contrib.admin import ModelAdmin, site
from core.models import MessageModel, RoomModel


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ("timestamp",)
    search_fields = ("id", "body", "user__username")
    list_display = ("id", "user", "group", "timestamp", "characters")
    list_display_links = ("id",)
    list_filter = ("user", "group")
    date_hierarchy = "timestamp"


class RoomModelAdmin(ModelAdmin):
    list_display = (
        "base_group",
        # "members",
    )


site.register(MessageModel, MessageModelAdmin)
site.register(RoomModel, RoomModelAdmin)
