# Generated by Django 5.2.3 on 2025-07-21 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_orderupdate_timestamp_alter_orderupdate_update_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderupdate',
            name='timestamp',
        ),
    ]
