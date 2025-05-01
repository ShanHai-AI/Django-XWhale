from django.urls import path
from . import views

app_name = 'agentApp'

urlpatterns = [
    path('status/', views.status, name='status'),  #获取状态
]