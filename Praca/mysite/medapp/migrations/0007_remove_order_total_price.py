# Generated by Django 3.2.8 on 2021-12-12 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0006_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]
