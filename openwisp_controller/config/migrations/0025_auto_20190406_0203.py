# Generated by Django 2.0.13 on 2019-04-06 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0024_auto_20190404_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='template',
            name='url',
        ),
        migrations.RemoveField(
            model_name='template',
            name='variable',
        ),
    ]