# Generated by Django 3.1.7 on 2021-05-17 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20210517_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='assigned_to',
        ),
    ]
