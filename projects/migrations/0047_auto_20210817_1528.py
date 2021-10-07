# Generated by Django 3.1.7 on 2021-08-17 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0046_fieldmanagerassignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldmanagerassignment',
            name='supervisor_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='field_manager_assignment', to=settings.AUTH_USER_MODEL),
        ),
    ]
