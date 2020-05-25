from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NoseyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("point", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("point", self.channel_name)
        print(f"Removed {self.channel_name} channel to gossip")

    async def bash_script(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")