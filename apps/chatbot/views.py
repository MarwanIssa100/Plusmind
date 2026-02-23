from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .ai import ask_groq, update_user_memory
from .prompt import CRISIS_RESPONSE
from .models import Conversation, Message

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_view(request):

    message = request.data.get("message")
    convo_id = request.data.get("conversation_id")

    if not message:
        return Response({"error": "message is required"}, status=400)

    user = request.user   # 🔥 الآن يعمل مع JWT

    # create or get conversation
    if not convo_id:
        conversation = Conversation.objects.create(user=user)
    else:
        conversation = Conversation.objects.filter(id=convo_id, user=user).first()
        if not conversation:
            return Response({"error": "conversation not found"}, status=404)

    # save user message first
    Message.objects.create(
        conversation=conversation,
        role="user",
        content=message
    )

    # get last 6 messages
    previous_messages = Message.objects.filter(
        conversation=conversation
    ).order_by("-created_at")[:6]

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(previous_messages)
    ]

    # AI reply
    reply = ask_groq(message, history, user=user)
    # update memory every 8 messages
    msg_count = Message.objects.filter(conversation=conversation).count()
    if msg_count % 8 == 0:
        update_user_memory(user, conversation)

    # don't store crisis message
    if reply != CRISIS_RESPONSE:
        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=reply
        )

    return Response({
        "reply": reply,
        "conversation_id": conversation.id
    })