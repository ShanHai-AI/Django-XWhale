from django.db import models


# Create your models here.
class Award(models.Model):  # 荣誉模型
    description = models.TextField(max_length=500,
                                   blank=True,
                                   null=True,
                                   verbose_name='成果简介')
    photo = models.ImageField(upload_to='Award/',
                              blank=True,
                              verbose_name='成果图片')

    class Meta:
        verbose_name = '成果简介'
        verbose_name_plural = '成果简介'
