# Generated by Django 2.2.1 on 2020-12-17 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0045_auto_20201216_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wagesheet',
            old_name='is_manager_approved',
            new_name='manager_status',
        ),
        migrations.RenameField(
            model_name='wagesheet',
            old_name='is_project_manager_approved',
            new_name='project_manager_status',
        ),
    ]
