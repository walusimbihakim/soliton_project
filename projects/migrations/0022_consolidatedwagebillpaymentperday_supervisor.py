# Generated by Django 3.1.7 on 2021-05-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20210524_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidatedwagebillpaymentperday',
            name='supervisor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
