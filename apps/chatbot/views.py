
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .ai import ask_groq, update_user_memory
from .prompt import CRISIS_RESPONSE

ANON_MESSAGE_LIMIT = 3
ANON_CHAT_COUNT_KEY = "anon_chat_count"


class ChatbotAPIView(APIView):
    """
    Handles chatbot messages.

    - Anonymous users: limited to 3 messages, tracked via session,
      conversations NOT persisted to the database.
    - Authenticated users: unlimited messages, conversations saved normally.
    """

    @swagger_auto_schema(
        operation_description=(
            "Send a chat message to the chatbot. Anonymous users are limited to "
            "3 messages per session; authenticated users have no limit and their "
            "conversation is persisted."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["message"],
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User message to the chatbot",
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Bot reply",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "reply": openapi.Schema(type=openapi.TYPE_STRING),
                        "messages_used": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Only for anonymous users",
                        ),
                        "messages_remaining": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Only for anonymous users",
                        ),
                    },
                    required=["reply"],
                ),
            ),
            400: openapi.Response(
                description="Message cannot be empty",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            ),
            403: openapi.Response(
                description="Anonymous message limit reached",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            ),
        },
        tags=["Chatbot"],
    )
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message", "").strip()

        if not user_message:
            return Response(
                {"detail": "Message cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── ANONYMOUS BRANCH ──────────────────────────────────────────────
        if not request.user.is_authenticated:
            # Read current count (default 0 if session key absent)
            anon_count = request.session.get(ANON_CHAT_COUNT_KEY, 0)

            if anon_count >= ANON_MESSAGE_LIMIT:
                return Response(
                    {
                        "detail": (
                            "You have reached the free message limit. "
                            "Please login to continue chatting."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Increment BEFORE processing so a crash/retry can't give
            # the user an extra free message (fail-closed approach).
            request.session[ANON_CHAT_COUNT_KEY] = anon_count + 1
            request.session.modified = True   # force Django to persist

            # Generate bot reply without persistence or memory
            bot_reply = ask_groq(user_message)

            return Response(
                {
                    "reply": bot_reply,
                    "messages_used": request.session[ANON_CHAT_COUNT_KEY],
                    "messages_remaining": ANON_MESSAGE_LIMIT - request.session[ANON_CHAT_COUNT_KEY],
                },
                status=status.HTTP_200_OK,
            )

        # ── AUTHENTICATED BRANCH ──────────────────────────────────────────
        # Retrieve or create the user's active conversation
        conversation = (
            Conversation.objects.filter(user=request.user)
            .order_by("-created_at")
            .first()
        )
        if conversation is None:
            conversation = Conversation.objects.create(user=request.user)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_message,
        )

        # Build short history (last 6 messages) for the model
        previous_messages = Message.objects.filter(
            conversation=conversation
        ).order_by("-created_at")[:6]
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(previous_messages)
        ]

        # Generate bot reply
        bot_reply = ask_groq(user_message, history, user=request.user)

        # Save bot message unless it's a crisis response
        if bot_reply != CRISIS_RESPONSE:
            Message.objects.create(
                conversation=conversation,
                role="assistant",
                content=bot_reply,
            )

        # Update long-term memory every 8 messages
        msg_count = Message.objects.filter(conversation=conversation).count()
        if msg_count % 8 == 0:
            update_user_memory(request.user, conversation)

        return Response(
            {"reply": bot_reply},
            status=status.HTTP_200_OK,
        )

    # ------------------------------------------------------------------
    # Internal helper – replace the body with your real AI call
    # ------------------------------------------------------------------
    def _get_bot_reply(self, user_message: str) -> str:
        """
        Deprecated. Use ask_groq directly.
        """
        return ask_groq(user_message)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .ai import ask_groq, update_user_memory
# from .prompt import CRISIS_RESPONSE
# from .models import Conversation, Message

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def chat_view(request):

#     message = request.data.get("message")
#     convo_id = request.data.get("conversation_id")

#     if not message:
#         return Response({"error": "message is required"}, status=400)

#     user = request.user   # 🔥 الآن يعمل مع JWT

#     # create or get conversation
#     if not convo_id:
#         conversation = Conversation.objects.create(user=user)
#     else:
#         conversation = Conversation.objects.filter(id=convo_id, user=user).first()
#         if not conversation:
#             return Response({"error": "conversation not found"}, status=404)

#     # save user message first
#     Message.objects.create(
#         conversation=conversation,
#         role="user",
#         content=message
#     )

#     # get last 6 messages
#     previous_messages = Message.objects.filter(
#         conversation=conversation
#     ).order_by("-created_at")[:6]

#     history = [
#         {"role": msg.role, "content": msg.content}
#         for msg in reversed(previous_messages)
#     ]

#     # AI reply
#     reply = ask_groq(message, history, user=user)
#     # update memory every 8 messages
#     msg_count = Message.objects.filter(conversation=conversation).count()
#     if msg_count % 8 == 0:
#         update_user_memory(user, conversation)

#     # don't store crisis message
#     if reply != CRISIS_RESPONSE:
#         Message.objects.create(
#             conversation=conversation,
#             role="assistant",
#             content=reply
#         )

#     return Response({
#         "reply": reply,
#         "conversation_id": conversation.id
#     })
