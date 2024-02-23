from django.contrib import admin

from chats import models

# Register your models here.

admin.site.register(models.ShopUser)
admin.site.register(models.VisitorUser)
admin.site.register(models.ChatRoom)
admin.site.register(models.Message)