from django.contrib import admin
from .models import Room,Message,ForumCategory,ForumMessage,ForumMessageReport,Connected


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(ForumCategory)
admin.site.register(ForumMessage)
admin.site.register(ForumMessageReport)
admin.site.register(Connected)