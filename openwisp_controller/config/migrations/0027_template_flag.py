# Generated by Django 2.0.13 on 2019-04-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0026_template_variable'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='flag',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('shared_secret', 'Shared Secret')], default='private', help_text='Please choose if this template should be Public, Private or shared secretly', max_length=16, verbose_name='Flag'),
        ),
    ]
