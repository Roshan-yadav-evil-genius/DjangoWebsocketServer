from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer

class JsonConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # add the user to the group
        await self.channel_layer.group_add("TheMedium", self.channel_name)
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("TheMedium", self.channel_name)
        raise StopConsumer()
    
    async def receive_json(self, content):
        # Send message to group with sender's channel name
        await self.channel_layer.group_send("TheMedium", {
            "type": "chat.message",
            "message": content,
            "sender_channel_name": self.channel_name,
        })
    
    async def chat_message(self, event):
        message = event["message"]
        sender_channel_name = event["sender_channel_name"]
        
        # Send message to everyone except the sender
        if self.channel_name != sender_channel_name:
            await self.send_json(message)

# settings.py
