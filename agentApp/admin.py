from django.contrib import admin
from .models import Agent


# Register your models here.
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'agentID','function','status','photo']


admin.site.register(Agent, AgentAdmin)