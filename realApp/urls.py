from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'realApp'

urlpatterns = [
    path('register/', views.registrer, name='registrer'),
    path('visualization/', views.visualization, name='visualization'),
    path('report/', views.report, name='report'),
    path('agentV/', views.agentV, name='agentV'),
    path('get_b_changes/', views.get_b_changes, name='get_b_changes'),
    path('get_e_changes/', views.get_e_changes, name='get_e_changes'),
    path('a_week/', views.get_alerts_number_in_a_week, name='get_alerts_number_in_a_week'),
    path('agent_control/',views.agent_control, name='agent_control'),
    path('api_get_user/',views.api_get_user, name='api_get_user'),
    path('api_start/',views.api_start, name='api_start'),


]
# 添加以下代码以支持媒体文件的访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)