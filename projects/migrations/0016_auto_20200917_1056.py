# Generated by Django 2.2.1 on 2020-09-17 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20200914_0852'),
        ('projects', '0015_auto_20200916_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='survey',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='survey',
            name='scope',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='unit_of_measure',
            field=models.CharField(default='km', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='clientactivityrate',
            unique_together={('client', 'activity')},
        ),
    ]
