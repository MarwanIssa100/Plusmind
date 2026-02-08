import os
from dotenv import load_dotenv
from groq import Groq
from django.conf import settings

# Load .env from Django project root (folder that contains manage.py)
load_dotenv(settings.BASE_DIR / ".env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

GROQ_MODEL = "openai/gpt-oss-120b"


# normal response (for HTTP views)
def ask_groq(message):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to your .env file. "
            "Get a key at https://console.groq.com"
        )

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        err = str(e).strip().lower()
        if "connection" in err or "connect" in err:
            raise RuntimeError(
                "Could not reach Groq API. Check: 1) GROQ_API_KEY in .env is valid, "
                "2) your internet connection, 3) firewall/proxy."
            ) from e
        raise


# streaming response (for websocket)
def stream_groq(message):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": message}
        ],
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
