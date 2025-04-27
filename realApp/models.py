from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    phoneID = models.CharField(max_length=30, verbose_name='电话号码')
    sex = models.CharField(max_length=5, default='男', verbose_name='性别')
    experience = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='描述')
    photo = models.ImageField(upload_to='contact/recruit/%Y_%m_%d',
                              verbose_name='个人照片')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '注册信息'
        verbose_name_plural = '注册信息'
        ordering = ('-publishDate',)




class Alerts(models.Model):
    alert_type = (
        (1, '心理状态'),
        (2, '行为状态'),
    )
    status = models.IntegerField(choices=alert_type,
                                 default=1,
                                 verbose_name='预警类型')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')
    content = models.TextField(blank=True, null=True, verbose_name='预警描述')
    photo = models.ImageField(upload_to='image_warning/alerts/%Y_%m_%d', blank=True, null=True, verbose_name='预警照片')
    video = models.FileField(upload_to='video_warning/alerts/%Y_%m_%d', blank=True, null=True, verbose_name='预警视频')
    strategy = models.TextField(blank=True, null=True, verbose_name='采取策略')
    short_message = models.CharField(max_length=30, default="",verbose_name='短信通知')

    class Meta:
        verbose_name = '预警信息'
        verbose_name_plural = '预警信息'
        ordering = ('-publishDate',)


class EmotionChange(models.Model):
    alert_type = (
        (1, '平静'),
        (2, '喜悦'),
        (3, '痛苦悲伤'),
    )
    status = models.IntegerField(choices=alert_type,
                                 default=1,
                                 verbose_name='预警类型')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')


    class Meta:
        verbose_name = '情绪状态变化'
        verbose_name_plural = '情绪状态变化'
        ordering = ('-publishDate',)

class BehaviorChange(models.Model):
    alert_type = (
        (1, '跌倒'),
        (2, '捂胸口'),
        (3, '扶墙'),
        (4, '其他'),
    )
    status = models.IntegerField(choices=alert_type,
                                 default=1,
                                 verbose_name='预警类型')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')

    class Meta:
        verbose_name = '行为状态变化'
        verbose_name_plural = '行为状态变化'
        ordering = ('-publishDate',)
