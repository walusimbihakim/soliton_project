# Generated by Django 3.1.7 on 2021-05-18 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20210518_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='assigned_to',
        ),
    ]
