# Generated by Django 3.2.8 on 2021-12-09 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0004_auto_20211209_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email_guest',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message_text',
            field=models.TextField(),
        ),
    ]