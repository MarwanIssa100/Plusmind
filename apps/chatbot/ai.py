import os
import re
from dotenv import load_dotenv
from groq import Groq
from django.conf import settings
from .prompt import SYSTEM_PROMPT, CRISIS_RESPONSE
from .models import Conversation, Message, UserMemory  # used by stream_groq / other callers

# Load .env from Django project root (folder that contains manage.py)
load_dotenv(settings.BASE_DIR / ".env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

GROQ_MODEL = "openai/gpt-oss-120b"


# --------- CRISIS DETECTION ---------

SUICIDE_PATTERNS = [
    r"انتحر",
    r"اموت",
    r"عايز اموت",
    r"مش عايز اعيش",
    r"هقتل نفسي",
    r"انهي حياتي",
    r"مش قادر اكمل",
    r"تعبت من حياتي",
    r"نفسي اختفي",
    r"i want to die",
    r"kill myself",
    r"suicide",
    r"end my life",
]

def is_crisis(message) -> bool:
    if not isinstance(message, str):
        return False
    message = message.lower()
    return any(re.search(pattern, message) for pattern in SUICIDE_PATTERNS)


# --------- NORMAL RESPONSE (HTTP) ---------
def ask_groq(message, history=None, user=None):
    # Ensure message is a string (client may send a list)
    if isinstance(message, list):
        message = message[0] if message else ""
    message = str(message) if message else ""

    # 🔴 CRISIS CHECK
    if is_crisis(message):
        return CRISIS_RESPONSE

    history = history or []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Inject long-term memory when user is provided
    if user:
        memory_obj, _ = UserMemory.objects.get_or_create(user=user)
        if memory_obj.summary:
            messages.append({
                "role": "system",
                "content": f"User background information:\n{memory_obj.summary}"
            })
    messages.extend(history[-6:])  # last 6 only
    messages.append({
        "role": "system",
        "content": "Reminder: reply briefly in Egyptian Arabic dialect, max 4 sentences."
    })
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.4,
        max_completion_tokens=180,
        top_p=0.9,
        presence_penalty=0.3,
        frequency_penalty=0.6,
    )

    reply = completion.choices[0].message.content
    return reply

def update_user_memory(user, conversation):

    messages = Message.objects.filter(
        conversation=conversation
    ).order_by("-created_at")[:12]

    chat_text = "\n".join([
        f"{m.role}: {m.content}" for m in reversed(messages)
    ])

    memory_prompt = f"""
You are extracting long-term memory about a user.

From the conversation below, write short bullet points describing:
- recurring problems
- stress sources
- relationships
- coping methods
- important life events

Write VERY SHORT bullet points only.

Conversation:
{chat_text}
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": memory_prompt}],
        temperature=0.2,
        max_completion_tokens=200
    )

    new_summary = completion.choices[0].message.content

    memory_obj, _ = UserMemory.objects.get_or_create(user=user)

    memory_obj.summary = new_summary
    memory_obj.save()

# --------- STREAMING RESPONSE (WEBSOCKET) ---------

def stream_groq(message, history=None):
    if isinstance(message, list):
        message = message[0] if message else ""
    message = str(message) if message else ""

    # 🔴 CRISIS INTERCEPTOR للويب سوكيت
    if is_crisis(message):
        yield CRISIS_RESPONSE
        return

    # نفس بناء الرسائل
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    MAX_HISTORY = 6
    if history:
        messages.extend(history[-MAX_HISTORY:])

    messages.append({
        "role": "system",
        "content": "Reminder: reply briefly in Egyptian Arabic dialect, max 4 sentences."
    })

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.4,
        max_completion_tokens=180,
        top_p=0.9,
        presence_penalty=0.3,
        frequency_penalty=0.6,
        stream=True
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
