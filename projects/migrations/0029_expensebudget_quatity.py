# Generated by Django 2.2.1 on 2020-09-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20200928_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensebudget',
            name='quatity',
            field=models.IntegerField(default=0),
        ),
    ]