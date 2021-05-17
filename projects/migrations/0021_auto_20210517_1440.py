# Generated by Django 3.1.7 on 2021-05-17 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_workerassignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workerassignment',
            old_name='supervisor',
            new_name='from_supervisor',
        ),
        migrations.AddField(
            model_name='workerassignment',
            name='to_supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_supervisor', to=settings.AUTH_USER_MODEL),
        ),
    ]
