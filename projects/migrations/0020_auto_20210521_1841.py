# Generated by Django 3.1.7 on 2021-05-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20210519_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consolidatedwagebill',
            name='worker_mobile_money_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]