# Generated by Django 2.2.2 on 2020-09-17 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20200917_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='executionscope',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]