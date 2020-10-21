release: python manage.py migrate
web: daphne chat.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
