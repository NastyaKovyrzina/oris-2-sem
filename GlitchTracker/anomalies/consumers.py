import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "glitchtracker_chat"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Аноним"
        self.send(text_data=json.dumps({
            "message": f"Привет, {name}! Добро пожаловать в чат GlitchTracker!"
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        data = json.loads(text_data)
        message = data.get("message", "")
        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Анонимус"
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{name}: {message}",
            },
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))