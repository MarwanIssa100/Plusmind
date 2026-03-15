# from django.urls import re_path
# from .consumer import chatConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/chatbot/', chatConsumer.as_asgi()),
# ]

from django.urls import path
from .views import ChatbotAPIView

urlpatterns = [
    # path("", chat_view, name="chat_api"),
    path("", ChatbotAPIView.as_view(), name="chatbot"),
]
