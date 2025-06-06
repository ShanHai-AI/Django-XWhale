# Generated by Django 5.1.4 on 2025-04-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutApp', '0002_auto_20190921_1221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={'verbose_name': '成果', 'verbose_name_plural': '成果'},
        ),
        migrations.AlterField(
            model_name='award',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='成果简介'),
        ),
        migrations.AlterField(
            model_name='award',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='award',
            name='photo',
            field=models.ImageField(blank=True, upload_to='Award/', verbose_name='成果图片'),
        ),
    ]
