# Generated by Django 2.0.13 on 2019-04-04 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0019_organization_mac_add_hardware_id_name_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='context',
        ),
    ]
