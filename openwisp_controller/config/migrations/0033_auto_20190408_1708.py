# Generated by Django 2.0.13 on 2019-04-08 15:08

import django.core.validators
from django.db import migrations, models
import jsonfield.fields
import re


class Migration(migrations.Migration):

    dependencies = [
        ('openwisp_users', '0004_default_groups'),
        ('config', '0032_auto_20190406_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='context',
            field=jsonfield.fields.JSONField(blank=True, help_text='Additional <a href="http://netjsonconfig.openwisp.org/en/stable/general/basics.html#context" target="_blank">context (configuration variables)</a> in JSON format', null=True),
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
            unique_together={('name', 'organization'), ('mac_address', 'organization'), ('hardware_id', 'organization')},
        ),
    ]