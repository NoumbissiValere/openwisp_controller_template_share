# Generated by Django 2.0.10 on 2019-01-17 19:28

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('openwisp_users', '0004_default_groups'),
        ('config', '0018_config_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='hardware_id',
            field=models.CharField(blank=True, help_text='Serial number of this device', max_length=32, null=True, unique=True, verbose_name='Serial number'),
        ),
        migrations.AlterField(
            model_name='device',
            name='mac_address',
            field=models.CharField(db_index=True, help_text='primary mac address', max_length=17, validators=[django.core.validators.RegexValidator(re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'), code='invalid', message='Must be a valid mac address.')]),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together={('hardware_id', 'organization'), ('mac_address', 'organization'), ('name', 'organization')},
        ),
    ]
