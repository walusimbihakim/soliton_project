# Generated by Django 3.1.4 on 2020-12-31 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0044_auto_20201231_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='wagesheet',
            name='segment',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='projects.segment'),
        ),
    ]