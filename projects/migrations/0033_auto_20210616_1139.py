# Generated by Django 3.1.7 on 2021-06-16 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20210616_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wagesheet',
            options={'ordering': ('date', 'supervisor_user__first_name')},
        ),
    ]
