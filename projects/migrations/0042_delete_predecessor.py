# Generated by Django 2.2.1 on 2020-10-30 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_pip_dependencies'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Predecessor',
        ),
    ]