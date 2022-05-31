from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'role']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'title', 'price', 'category', 'status']


class TaskRespAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'task_id', 'resp_text']

class BotMessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'message']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskResp, TaskRespAdmin)
admin.site.register(BotMessage, BotMessageAdmin)
