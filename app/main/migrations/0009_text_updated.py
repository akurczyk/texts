# Generated by Django 2.1 on 2018-08-27 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180827_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
