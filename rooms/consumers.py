import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from .models import Room,Message,Connected
from django.utils.text import slugify

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.connect_user(room_name=self.room_name, user=self.scope['user'])
        

        
        
        


    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.disconnect_user(room_name=self.room_name, user=self.scope['user'])

       

       

        
        

   
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)
        profile = await self.get_user_profile()
        profile_pic = profile.image.url

       
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile_pic': profile_pic,
                
                
            }
        )

    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        profile_pic = event['profile_pic']
        
        

        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'profile_pic': profile_pic,
            
            
        }))



    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
      
        Message.objects.create(user=user, room=room, content=message)

    

    @database_sync_to_async
    def get_user_profile(self):
        
        return self.scope['user'].profile
    



    @sync_to_async
    def connect_user(self,room_name, user):
        room_slug = slugify(room_name)
        room = Room.objects.get(slug=room_slug)

        if user:
         object, created =  Connected.objects.get_or_create(user=user, room_name=room)
        else:
            pass
        return None


    @sync_to_async
    def disconnect_user(self,room_name, user):

        room_slug = slugify(room_name)
        room = Room.objects.get(slug=room_slug)

        if user:
            try:
                get_object_or_404(Connected, Q(user=user), Q(room_name=room))
            except:
                pass
            else:
                user = get_object_or_404(Connected, Q(user=user), Q(room_name=room))
                user.delete()
        return None

    

  



    



 

