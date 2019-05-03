# Generated by Django 2.0.13 on 2019-05-03 10:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0022_auto_20190430_0710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subscriber', models.URLField(db_index=True, max_length=16, verbose_name='Subscriber domain')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Template')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unsubscribe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subscriber', models.URLField(db_index=True, max_length=16, verbose_name='Subscriber domain')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Template')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
