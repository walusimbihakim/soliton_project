# Generated by Django 2.2.2 on 2020-10-16 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20201016_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('payment', models.IntegerField()),
                ('pip_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.PIP')),
                ('wage_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.WageSheet')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Worker')),
            ],
            options={
                'unique_together': {('worker', 'pip_activity')},
            },
        ),
        migrations.DeleteModel(
            name='Wages',
        ),
    ]