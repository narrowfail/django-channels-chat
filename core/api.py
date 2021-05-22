from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from chat import settings
from core.serializers import (
    MessageModelSerializer,
    UserModelSerializer,
    RoomModelSerializer,
)
from core.models import MessageModel, RoomModel


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """

    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ("GET", "POST", "HEAD", "OPTIONS")
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(group=self.request.query_params["target"])
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     msg = get_object_or_404(
    #         self.queryset.filter(
    #             Q(recipient=request.user) | Q(user=request.user), Q(pk=kwargs["pk"])
    #         )
    #     )
    #     serializer = self.get_serializer(msg)
    #     return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ("GET", "HEAD", "OPTIONS")
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)


class RoomModelViewSet(ModelViewSet):
    queryset = RoomModel.objects.all()
    serializer_class = RoomModelSerializer
    allowed_methods = "GET"
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        self.queryset = RoomModel.objects.filter(members=request.user)
        return super(RoomModelViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        group_name = request.data["room_name"]
        user_list = User.objects.all()

        new_group = Group.objects.create(name=get_random_string())
        room = RoomModel(title=get_random_string())
        room.base_group = new_group
        room.save()  # must be saved first!

        for u in user_list:
            room.members.add(u)
        room.save()

        return Response(status=200)
