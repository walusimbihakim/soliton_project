# Generated by Django 3.1.7 on 2021-05-01 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20210501_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worker',
            old_name='national_id_NIN',
            new_name='national_ID_NIN',
        ),
        migrations.RenameField(
            model_name='worker',
            old_name='national_id_document',
            new_name='national_ID_document',
        ),
    ]