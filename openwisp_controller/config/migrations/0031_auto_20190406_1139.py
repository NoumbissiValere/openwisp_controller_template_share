# Generated by Django 2.0.13 on 2019-04-06 09:39

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_auto_20190406_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='variable',
            field=jsonfield.fields.JSONField(blank=True, default=dict, help_text='Provide values for the list of variables found at the detail page of this template at the Library', null=True, verbose_name='context'),
        ),
    ]
