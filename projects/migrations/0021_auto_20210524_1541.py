# Generated by Django 3.1.7 on 2021-05-24 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20210521_1841'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConsolidatedWageBill',
            new_name='ConsolidatedWageBillPayment',
        ),
        migrations.RenameModel(
            old_name='ConsolidatedWageBillPerDay',
            new_name='ConsolidatedWageBillPaymentPerDay',
        ),
    ]
