import json
# json.dumps : native -> json
# json.loads: json -> native
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message_content = data['message']
        new_message = Message.objects.create(author=author_user, content=message_content)
        new_message.save()
        message_json = self.message_to_json(new_message)
        return self.send_message_to_room(message_json)
    
    def message_to_json(self, message):
        my_timestamp = json.dumps(message.timestamp, indent=4, sort_keys=True, default=str)
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': my_timestamp
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_room_name = "chat_%s" % self.room_name  # construct the group name

        async_to_sync(self.channel_layer.group_add)(
            self.group_room_name,
            self.channel_name
        )
        async_to_sync(self.accept())

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_native_obj = json.loads(text_data)
        self.new_message(text_data_native_obj)

    def send_message_to_room(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.group_room_name,
            {
                "type": "chat_message", 
                "data": data
            }
        )

    # method that will be invoked on the Consumer that receives the event
    def chat_message(self, event):
        data = event['data']
        self.send(json.dumps({
            'data': data
        }))
