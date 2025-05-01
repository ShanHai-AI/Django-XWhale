import pinyin
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import Alerts, EmotionChange, BehaviorChange, Resume,IP_Config
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .forms import ResumeForm
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def registrer(request):
    if request.method == 'POST':
        print()
        resumeForm = ResumeForm(data=request.POST, files=request.FILES)
        # print(resumeForm)
        print(resumeForm.errors)
        if resumeForm.is_valid():
            # 先保存数据，得到实例对象
            resume = resumeForm.save(commit=False)

            # 处理照片：优先判断是否是拍照上传的 base64 数据
            photo_data = request.POST.get('photo_data')  # 来自前端 canvas 转换的照片

            if photo_data:
                print("拍照上传")
                try:
                    # 分离格式和数据部分
                    format, imgstr = photo_data.split(';base64,')
                    ext = format.split('/')[-1]  # 获取扩展名，如 png/jpg

                    # 中文转拼音
                    name = pinyin.get(resume.name, format='strip')
                    # 使用姓名作为文件名避免冲突（生产环境建议加 UUID）
                    file_name = f"{name}.{ext}"

                    # 解码并保存为 Django 的 ImageField
                    data = ContentFile(base64.b64decode(imgstr), name=file_name)
                    resume.photo.save(file_name, data, save=False)  # save=False 防止提前写入数据库
                except Exception as e:
                    print("图片解析失败：", e)
                    # 可选：添加错误提示给前端
            elif 'photo' in request.FILES:
                # 如果用户选择了本地文件上传，则走原流程
                resume.photo = request.FILES['photo']
            else:
                # 两种方式都未提供照片时可设置默认值或抛出错误
                print("未提供照片")

            # 最终保存整个记录
            resume.save()

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
        }
    )


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


def agent_control(request):
    return render(request,'agent_control.html')

# 获取人员信息
def api_get_user(request):
    resume=Resume.objects.all()
    user_list=[]
    for i,user in enumerate(resume):
        user_list.append({"id": i, "name": user.name, "phone": user.phoneID, "image_url": user.photo.url})
    return JsonResponse(user_list, safe=False)


def get_img_b64(file_path):
    with open(file_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    return image_b64


def api_start(request):
    resume=Resume.objects.all()
    ipconfig=IP_Config.objects.filter(name="Agent1")
    print(request.body)
    user_list=[]
    for i,user in enumerate(resume):
        user_list.append({"id": i, "name": user.name, "phone": user.phoneID, "image_url": user.photo.url})

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')

        if user_id is None:
            return JsonResponse({'error': '缺少 user_id'}, status=400)

        # 这里可以添加你的业务逻辑
        print(f"收到启动请求，用户ID: {user_id}")
        follow_img= "/Users/liqiang/Downloads/Project/Django-XWhale/"+user_list[user_id]["image_url"]
        print(follow_img)
        img_b64 = get_img_b64(follow_img)
        data = {
            # "person_describe_str": res,  # 示例参数
            "img_b64": img_b64
        }

        response = requests.post(
            url = f"http://{ipconfig[0].ip}:16532/start_tracking",
            json=data,  # 自动序列化为JSON
            headers={"Content-Type": "application/json"}
        )

        if response.status_code:
            return JsonResponse({
                'message': f'已启动跟踪用户 ID: {user_list[user_id]["name"]}',
                'status': 'success'
            })
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    # else:
    #     return JsonResponse({'error': '仅支持 POST 请求'}, status=405)

