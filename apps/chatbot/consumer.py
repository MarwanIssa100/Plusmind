import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

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

        #call groq api 
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[ {"role": "user", "content": message} ],
            stream=True
        )

        ai_reply = ""

        for chunk in response:
            if chunk.choices[0].delta.content:
                ai_reply += chunk.choices[0].delta.content

                await self.send(text_data=json.dumps({
                    "type": "assistant",
                    "message": ai_reply
                }))