# Generated by Django 2.2.2 on 2020-09-18 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_executionscope_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='executionscope',
            unique_together=set(),
        ),
    ]
