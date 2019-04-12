# Generated by Django 2.0.13 on 2019-04-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0023_auto_20190404_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='flag',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('shared_secret', 'Shared Secret'), ('import', 'Import')], db_index=True, default='private', help_text='Whether this template can be shared, remain private or will be imported', max_length=16, verbose_name='flag'),
        ),
    ]