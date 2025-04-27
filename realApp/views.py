from django.shortcuts import render,HttpResponse
from .forms import ResumeForm
from django.http import JsonResponse
from .models import Alerts, EmotionChange, BehaviorChange, Resume
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

# Create your views here.
def registrer(request):
    if request.method == 'POST':
        resumeForm = ResumeForm(data=request.POST, files=request.FILES)
        if resumeForm.is_valid():
            resumeForm.save()
            return render(request, 'success.html', {
                'active_menu': 'contactus',
                'sub_menu': 'recruit',
            })
    else:
        resumeForm = ResumeForm()
    return render(
        request, 'registrer.html', {
            'active_menu': 'contactus',
            'sub_menu': 'recruit',
            'resumeForm': resumeForm,
        })

def visualization(request):
    return render(request,'analysis.html')

def get_b_changes(request):
    behavior_status_list={
        "1":'跌倒',
        "2":'捂胸口',
        "3":'扶墙',
        "4":'其他',
    }
    behavior_weight_list = {
        "1": '0.3',
        "2": '0.2',
        "3": '0.2',
        "4": '0.1',
    }
    behavior_change=BehaviorChange.objects.all().order_by('-publishDate')
    data = [ {'name': behavior_status_list[str(behavior.status)],'value':[behavior.publishDate,behavior_weight_list[str(behavior.status)]]}
        for behavior in behavior_change],
    return JsonResponse(data, safe=False)


def get_e_changes(request):
    emotion_status_list={
        "1":'平静',
        "2":'喜悦',
        "3":'痛苦悲伤',
    }
    emotion_weight_list={
        "1":'0.5',
        "2":'0.3',
        "3":'0.8',
    }
    emotion_change=EmotionChange.objects.all().order_by('-publishDate')
    data = [ {'name': emotion_status_list[str(emotion.status)],'value':[emotion.publishDate,emotion_weight_list[str(emotion.status)]]} for emotion in emotion_change],
    return JsonResponse(data, safe=False)


def get_alerts_number_in_a_week(request):
    # 获取当前时间和一周前的时间
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # 查询最近一周内的所有预警记录
    alerts_in_week = Alerts.objects.filter(publishDate__gte=one_week_ago)

    # 按日期分组统计每天的预警次数
    alerts_by_date = defaultdict(int)
    for alert in alerts_in_week:
        date = alert.publishDate.date()  # 提取日期部分
        alerts_by_date[date] += 1

    # 构造返回数据
    data = [
        {"date": str(date), "count": count}
        for date, count in alerts_by_date.items()
    ]
    return JsonResponse(data, safe=False)

def report(request):
    emotion_alerts=Alerts.objects.all().filter(Q(status=1)).order_by('-publishDate')
    behavior_alerts=Alerts.objects.all().filter(Q(status=2)).order_by('-publishDate')
    # for emo in emotion_alerts:
    #     print(emo.publishDate,emo.content,emo.status,emo.short_message,emo.photo)
    return render(request,'report.html',{
        'emotion_alerts':emotion_alerts,
        'behavior_alerts':behavior_alerts,
        'num_emotion_alerts':len(emotion_alerts),
        'num_behavior_alerts':len(behavior_alerts)}
    )

def agentV(request):
    return render(request,'agentV.html')