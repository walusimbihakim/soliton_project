# Generated by Django 3.1.7 on 2021-03-15 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='mobile_money_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
