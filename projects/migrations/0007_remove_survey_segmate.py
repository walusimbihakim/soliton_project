# Generated by Django 3.1.7 on 2021-04-19 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210414_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='segmate',
        ),
    ]
