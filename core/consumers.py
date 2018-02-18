from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import allowed_hosts_only


@allowed_hosts_only
@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the user group
    Group('%s' % message.user.id).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    # Remove user group
    Group('%s' % message.user.id).discard(message.reply_channel)
