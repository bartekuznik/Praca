# Generated by Django 3.2.8 on 2021-12-14 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0010_auto_20211214_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
    ]
