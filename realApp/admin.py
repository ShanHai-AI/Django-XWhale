from django.contrib import admin
from .models import Resume, Alerts,EmotionChange,BehaviorChange
from django.utils.safestring import mark_safe

class ResumeAdmin(admin.ModelAdmin):
    list_display =  ('name', 'sex', 'phoneID','experience',  'image_data')

    def image_data(self, obj):
        return mark_safe(u'<img src="%s" width="120px" />' % obj.photo.url)

    image_data.short_description = u'个人照片'
# Register your models here.

class AlertsAdmin(admin.ModelAdmin):
    list_display = ('status', 'publishDate', 'content','photo',  'video','strategy','short_message')

class EmotionChangeAdmin(admin.ModelAdmin):
    list_display = ('status', 'publishDate')

class BehaviorChangeAdmin(admin.ModelAdmin):
    list_display = ('status', 'publishDate')

admin.site.register(Resume,ResumeAdmin)
admin.site.register(Alerts,AlertsAdmin)
admin.site.register(EmotionChange,EmotionChangeAdmin)
admin.site.register(BehaviorChange,BehaviorChangeAdmin)

