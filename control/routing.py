# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("ws", consumers.EchoConsumer.as_asgi()),
]