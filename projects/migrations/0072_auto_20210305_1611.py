# Generated by Django 2.2.2 on 2021-03-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0071_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_supervisor',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]