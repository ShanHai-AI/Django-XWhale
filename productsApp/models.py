from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    PRODUCTS_CHOICES = (
        ('智慧康养', '智慧康养'),
        ('智慧教育', '智慧教育'),
        ('智慧校园', '智慧校园'),
    )
    title = models.CharField(max_length=50, verbose_name=' 案例标题')
    description = models.TextField(verbose_name='案例详情描述')
    productType = models.CharField(choices=PRODUCTS_CHOICES,
                                   max_length=50,
                                   verbose_name='类型')
    price = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='产品价格')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '案例演示'
        verbose_name_plural = '案例演示'
        ordering = ('-publishDate', )


class ProductImg(models.Model):
    product = models.ForeignKey(Product,
                                related_name='productImgs',
                                verbose_name='案例演示',
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Product/',
                              blank=True,
                              verbose_name='案例图片')
    video = models.FileField(upload_to='ProductVideo/', blank=True, verbose_name='案例视频')

    class Meta:
        verbose_name = '案例图片'
        verbose_name_plural = '案例图片'