# Generated by Django 3.1.7 on 2021-05-05 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_auto_20210505_1247'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='groupwage',
            unique_together={('wage_sheet', 'group_worker', 'activity')},
        ),
    ]
