# Generated by Django 2.2.1 on 2020-09-30 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_expensebudget_quatity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expensebudget',
            old_name='quatity',
            new_name='quantity',
        ),
    ]