# Generated by Django 3.1.7 on 2021-05-18 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_delete_workerassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('from_supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_supervisor', to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.worker')),
            ],
            options={
                'verbose_name': 'WorkerAssignment',
                'verbose_name_plural': 'WorkerAssignments',
            },
        ),
    ]
