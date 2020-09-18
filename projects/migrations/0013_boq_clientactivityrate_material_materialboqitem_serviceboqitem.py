# Generated by Django 2.2.2 on 2020-09-14 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20200914_0852'),
        ('projects', '0012_survey_surveyresult_surveyresultcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('survey', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('uom', models.CharField(max_length=20)),
                ('unit_cost', models.IntegerField()),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('UGX', 'UGX')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceBOQItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Activity')),
                ('boq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BOQ')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialBOQItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('boq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.BOQ')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Material')),
            ],
        ),
        migrations.CreateModel(
            name='ClientActivityRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('UGX', 'UGX')], default='UGX', max_length=3)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Activity')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
        ),
    ]