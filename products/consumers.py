import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "notifications",  # Groupe utilisé dans le signal
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    async def product_notification(self, event):
        # Envoyer le message reçu par WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
