# Generated by Django 2.2.1 on 2020-09-18 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_pip_predecessor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predecessor',
            name='status',
        ),
    ]
