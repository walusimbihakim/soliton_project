# Generated by Django 2.2.1 on 2021-02-11 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0060_wagebill'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wagebill',
            unique_together={('start_date', 'end_date')},
        ),
    ]