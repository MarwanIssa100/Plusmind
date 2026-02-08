import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .ai import stream_groq


class chatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        #send user message to groq
        await self.send(text_data=json.dumps({
            "type": "user",
            "message": message
        }))

        # run streaming in background thread
        generator = await sync_to_async(lambda: list(stream_groq(message)))()

        ai_reply = ""

        for token in generator:
            ai_reply += token

            await self.send(text_data=json.dumps({
                "type": "assistant",
                "message": ai_reply
            }))