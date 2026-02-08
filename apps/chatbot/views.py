from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai import ask_groq
import json

@csrf_exempt
def chat_view(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get("message")

        if not message:
            return JsonResponse({"error": "Message required"}, status=400)

        # call groq
        reply = ask_groq(message)

        return JsonResponse({
            "user": message,
            "assistant": reply
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
