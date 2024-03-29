# Generated by Django 3.1.7 on 2021-07-29 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0044_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-sent_time',)},
        ),
        migrations.AlterModelOptions(
            name='wagesheet',
            options={'ordering': ('supervisor_user__first_name', 'date')},
        ),
        migrations.RenameField(
            model_name='deduction',
            old_name='amount',
            new_name='payment',
        ),
    ]
