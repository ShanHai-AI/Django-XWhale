from django.contrib import admin
from .models import Award

# Register your models here.


class AwardAdmin(admin.ModelAdmin):
    list_display = ['description', 'photo']


admin.site.register(Award, AwardAdmin)

admin.site.site_header = '深心智慧'
admin.site.site_title = '深心智慧后台管理系统'