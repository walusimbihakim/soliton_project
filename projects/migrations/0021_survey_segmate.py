# Generated by Django 2.2.1 on 2020-09-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_executionscope_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='segmate',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]