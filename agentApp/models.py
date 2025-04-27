from django.db import models
from django.utils import timezone

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=20, verbose_name='智能体名称')
    agentID = models.CharField(max_length=30, verbose_name='智能体编号')
    function = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='功能描述')
    photo = models.ImageField(upload_to='agent/%Y_%m_%d',
                              verbose_name='智能体照片')
    status_list = (
        (1, '待机'),
        (2, '工作'),
        (3, '完成工作'),
        (4, '充电'),
    )
    status = models.IntegerField(choices=status_list,
                                 default=1,
                                 verbose_name='当前状态')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '智能体'
        verbose_name_plural = '智能体'
        ordering = ('-publishDate',)