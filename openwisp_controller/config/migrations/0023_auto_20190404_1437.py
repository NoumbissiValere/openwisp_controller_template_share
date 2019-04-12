# Generated by Django 2.0.13 on 2019-04-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0022_auto_20190404_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='flag',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('shared_secret', 'Shared Secret'), ('import', 'Import')], db_index=True, default='import', help_text='Whether this template can be shared, remain private or will be imported', max_length=16, verbose_name='flag'),
        ),
    ]