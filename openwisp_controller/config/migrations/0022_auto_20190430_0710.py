# Generated by Django 2.0.13 on 2019-04-30 05:10

import django.core.validators
from django.db import migrations, models
import django_netjsonconfig.utils
import jsonfield.fields
import re


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_merge_20190430_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='context',
            field=jsonfield.fields.JSONField(blank=True, help_text='Additional <a href="http://netjsonconfig.openwisp.org/en/stable/general/basics.html#context" target="_blank">context (configuration variables)</a> in JSON format', null=True),
        ),
        migrations.AddField(
            model_name='template',
            name='description',
            field=models.TextField(blank=True, help_text='Enter public description of this template', null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='template',
            name='flag',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('shared_secret', 'Shared Secret'), ('import', 'Import')], db_index=True, default='private', help_text='Whether to keep this template private or make it public, shared secretly or imported', max_length=16, verbose_name='Flag'),
        ),
        migrations.AddField(
            model_name='template',
            name='key',
            field=models.CharField(db_index=True, default=django_netjsonconfig.utils.get_random_key, help_text='share template key', max_length=64, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[^\\s/\\.]+$'), code='invalid', message='Key must not contain spaces, dots or slashes.')]),
        ),
        migrations.AddField(
            model_name='template',
            name='notes',
            field=models.TextField(blank=True, help_text='Enter internal notes for the administrators', null=True, verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='template',
            name='url',
            field=models.URLField(blank=True, help_text='Enter URL to import template from', null=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='template',
            name='variable',
            field=jsonfield.fields.JSONField(blank=True, default=dict, help_text='Enter Values for the variables used by this template', verbose_name='Variable'),
        ),
    ]