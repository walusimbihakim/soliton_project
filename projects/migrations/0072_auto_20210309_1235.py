# Generated by Django 2.2.2 on 2021-03-09 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0071_worker_mobile_money_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='mobile_money_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
