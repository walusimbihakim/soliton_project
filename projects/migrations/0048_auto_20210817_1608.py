# Generated by Django 3.1.7 on 2021-08-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0047_auto_20210817_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidatedwagebillpayment',
            name='field_manager',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='consolidatedwagebillpayment',
            name='field_manager_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]