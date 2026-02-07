from django.urls import re_path
from .consumer import chatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chatbot/', chatConsumer.as_asgi()),
]